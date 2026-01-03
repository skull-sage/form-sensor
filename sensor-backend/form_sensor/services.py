"""
Business logic services for the semantic sensor API.
All core functionality is implemented here, separated from HTTP concerns.
"""

from typing import Dict, List, Tuple, Optional
from fastapi import HTTPException
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .validators import validate_name_id, validate_text_content, validate_paragraphs, validate_bulk_sensors


class SensorService:
    """Service class for managing text sensors and their embeddings."""
    
    def __init__(self, model, text_store: dict, sensor_data_list: dict):
        """
        Initialize the sensor service.
        
        Args:
            model: The sentence transformer model
            text_store: Dictionary storing original text content
            sensor_data_list: Dictionary storing (paragraph, embedding) pairs
        """
        self.model = model
        self.text_store = text_store
        self.sensor_data_list = sensor_data_list
    
    def check_model_availability(self) -> None:
        """
        Check if the sentence transformer model is available.
        
        Raises:
            HTTPException: If model is not available
        """
        if self.model is None:
            raise HTTPException(status_code=503, detail="Sentence transformer model is not available")
    
    def check_sensor_exists(self, name_id: str, operation: str = "access") -> None:
        """
        Check if a text sensor exists and provide descriptive error messages.
        
        Args:
            name_id: The sensor nameId to check
            operation: Description of the operation being performed
            
        Raises:
            HTTPException: If sensor doesn't exist or is in corrupted state
        """
        if name_id not in self.sensor_data_list:
            if name_id in self.text_store:
                # Edge case: text exists but no sensor data (corrupted state)
                raise HTTPException(
                    status_code=500,
                    detail=f"Text sensor '{name_id}' is in corrupted state (text exists but no sensor data). Please recreate the sensor."
                )
            else:
                # Normal case: sensor doesn't exist
                available_sensors = list(self.sensor_data_list.keys())
                if available_sensors:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Text sensor '{name_id}' not found. Available sensors: {', '.join(available_sensors)}"
                    )
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Text sensor '{name_id}' not found. No sensors have been created yet."
                    )
    
    def split_text_into_paragraphs(self, text: str) -> List[str]:
        """
        Split text into paragraphs by newlines.
        
        Args:
            text: The text to split
            
        Returns:
            List[str]: List of non-empty paragraphs
        """
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        return validate_paragraphs(paragraphs)
    
    def generate_embeddings(self, paragraphs: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for a list of paragraphs.
        
        Args:
            paragraphs: List of paragraph texts
            
        Returns:
            List[np.ndarray]: List of embeddings
            
        Raises:
            HTTPException: If embedding generation fails
        """
        self.check_model_availability()
        
        embeddings = []
        for i, paragraph in enumerate(paragraphs):
            try:
                embedding = self.model.encode(paragraph)
                embeddings.append(embedding)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error generating embedding for paragraph {i+1}: {str(e)}"
                )
        
        return embeddings
    
    def create_sensor(self, name_id: str, text: str) -> dict:
        """
        Create a new text sensor with embeddings.
        
        Args:
            name_id: Unique identifier for the sensor
            text: Text content to create sensor from
            
        Returns:
            dict: Creation result with paragraph count
        """
        # Validate inputs
        validated_name_id = validate_name_id(name_id)
        validated_text = validate_text_content(text)
        
        # Store original text
        self.text_store[validated_name_id] = validated_text
        
        # Split into paragraphs
        paragraphs = self.split_text_into_paragraphs(validated_text)
        
        # Generate embeddings
        embeddings = self.generate_embeddings(paragraphs)
        
        # Create paired data structure
        sensor_pairs = list(zip(paragraphs, embeddings))
        
        # Store paired data
        self.sensor_data_list[validated_name_id] = sensor_pairs
        
        return {
            "message": "Text sensor created",
            "paragraphs_count": len(sensor_pairs)
        }
    
    def bulk_create_sensors(self, sensors_dict: dict) -> dict:
        """
        Bulk create multiple text sensors.
        
        Args:
            sensors_dict: Dictionary of nameId -> text mappings
            
        Returns:
            dict: Results with created, skipped, and failed lists
        """
        # Validate bulk input
        validated_sensors = validate_bulk_sensors(sensors_dict)
        
        created = []
        skipped = []
        failed = []
        
        for name_id, text in validated_sensors.items():
            try:
                # Skip if sensor already exists
                if name_id in self.sensor_data_list:
                    skipped.append(name_id)
                    continue
                
                # Create the sensor
                self.create_sensor(name_id, text)
                created.append(name_id)
                
            except Exception as e:
                print(f"Error processing sensor {name_id}: {e}")
                failed.append(name_id)
        
        return {
            "created": created,
            "skipped": skipped,
            "failed": failed
        }
    
    def calculate_similarity(self, input_text: str, name_id: str) -> dict:
        """
        Calculate similarity between input text and stored sensor.
        
        Args:
            input_text: Text to check similarity for
            name_id: Sensor to compare against
            
        Returns:
            dict: Similarity result with confidence score and matched paragraph
        """
        # Validate inputs
        validated_name_id = validate_name_id(name_id)
        validated_text = validate_text_content(input_text, max_length=5000, field_name="input text")
        
        # Check if sensor exists
        self.check_sensor_exists(validated_name_id, "similarity check")
        
        # Generate embedding for input text
        try:
            input_embedding = self.model.encode(validated_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating embedding for input text: {str(e)}")
        
        # Get stored sensor data
        sensor_pairs = self.sensor_data_list[validated_name_id]
        
        if not sensor_pairs:
            raise HTTPException(status_code=404, detail=f"No sensor data found for text sensor '{validated_name_id}'")
        
        # Calculate similarities
        similarity_scores = []
        for paragraph, stored_embedding in sensor_pairs:
            try:
                # Reshape embeddings for cosine_similarity function
                input_emb_reshaped = input_embedding.reshape(1, -1)
                stored_emb_reshaped = stored_embedding.reshape(1, -1)
                
                # Calculate cosine similarity
                similarity = cosine_similarity(input_emb_reshaped, stored_emb_reshaped)[0][0]
                similarity_scores.append((similarity, paragraph))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error calculating similarity: {str(e)}")
        
        # Find best match
        best_match = max(similarity_scores, key=lambda x: x[0])
        highest_score, matched_paragraph = best_match
        
        return {
            "confidence_score": float(highest_score),
            "matched_paragraph": matched_paragraph
        }
    
    def get_all_sensors(self) -> dict:
        """
        Get all stored sensors.
        
        Returns:
            dict: All sensors with their text content and count
        """
        sensors_mapping = {}
        for name_id in self.sensor_data_list.keys():
            if name_id in self.text_store:
                sensors_mapping[name_id] = self.text_store[name_id]
        
        return {
            "sensors": sensors_mapping,
            "count": len(sensors_mapping)
        }
    
    def delete_sensor(self, name_id: str) -> dict:
        """
        Delete a text sensor.
        
        Args:
            name_id: Sensor to delete
            
        Returns:
            dict: Deletion confirmation message
        """
        # Validate nameId
        validated_name_id = validate_name_id(name_id)
        
        # Check if sensor exists
        self.check_sensor_exists(validated_name_id, "deletion")
        
        # Remove from both stores
        if validated_name_id in self.text_store:
            del self.text_store[validated_name_id]
        
        if validated_name_id in self.sensor_data_list:
            del self.sensor_data_list[validated_name_id]
        
        return {"message": f"Text sensor '{validated_name_id}' deleted successfully"}