from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import uvicorn
from typing import List, Dict
import json

app = FastAPI(
    title="Semantic Description Sensor API",
    description="API for semantic similarity detection using sentence transformers",
    version="1.0.0"
)

# Configure CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with descriptive messages"""
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_details.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation Error",
            "message": "Invalid input data",
            "details": error_details
        }
    )

@app.exception_handler(json.JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
    """Handle malformed JSON requests"""
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid JSON",
            "message": "Request body contains malformed JSON",
            "details": [str(exc)]
        }
    )

# Load the sentence transformer model
model = None
model_error = None

def load_model():
    """Load the sentence transformer model with proper error handling"""
    global model, model_error
    try:
        print("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        model_error = None
        print("Model loaded successfully")
        return True
    except Exception as e:
        error_msg = f"Failed to load sentence transformer model: {str(e)}"
        print(error_msg)
        model_error = error_msg
        model = None
        return False

# Try to load model on startup
load_model()

# In-memory storage for text sensors
text_store = {}  # nameId -> original full text
sensor_data_list = {}  # nameId -> [(paragraph, embedding), (paragraph, embedding), ...]

class CreateSensorRequest(BaseModel):
    text: str
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty or contain only whitespace')
        if len(v.strip()) > 10000:  # Reasonable limit for text length
            raise ValueError('Text is too long (maximum 10,000 characters)')
        return v.strip()

class SimilarityRequest(BaseModel):
    text: str
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty or contain only whitespace')
        if len(v.strip()) > 5000:  # Reasonable limit for similarity check text
            raise ValueError('Text is too long (maximum 5,000 characters)')
        return v.strip()

class SimilarityResponse(BaseModel):
    confidence_score: float
    matched_paragraph: str

class BulkCreateRequest(BaseModel):
    sensors: Dict[str, str]  # nameId -> text mapping

class BulkCreateResponse(BaseModel):
    created: List[str]  # list of successfully created sensor nameIds
    skipped: List[str]  # list of nameIds that already existed
    failed: List[str]   # list of nameIds that failed to create

class SensorListResponse(BaseModel):
    sensors: Dict[str, str]  # nameId -> text mapping
    count: int

@app.get("/")
async def root():
    return {"message": "Semantic Description Sensor API is running"}

@app.get("/health")
async def health_check():
    model_status = "loaded" if model is not None else "failed"
    health_status = "healthy" if model is not None else "degraded"
    
    response = {
        "status": health_status,
        "service": "semantic-sensor-api",
        "model": "all-MiniLM-L6-v2",
        "model_status": model_status
    }
    
    if model_error:
        response["model_error"] = model_error
    
    return response

@app.post("/reload-model")
async def reload_model():
    """Reload the sentence transformer model"""
    success = load_model()
    if success:
        return {"message": "Model reloaded successfully", "status": "loaded"}
    else:
        raise HTTPException(
            status_code=503, 
            detail=f"Failed to reload model: {model_error}"
        )

@app.post("/bulk-create-sensors", response_model=BulkCreateResponse)
async def bulk_create_sensors(request: BulkCreateRequest):
    """
    Bulk create text sensors from browser storage.
    Only creates sensors that don't already exist.
    """
    try:
        # Check if model is loaded
        check_model_availability()
        
        created = []
        skipped = []
        failed = []
        
        for name_id, text in request.sensors.items():
            try:
                # Validate nameId
                validated_name_id = validate_name_id(name_id)
                
                # Skip if sensor already exists
                if validated_name_id in sensor_data_list:
                    skipped.append(validated_name_id)
                    continue
                
                # Store original text mapping
                text_store[validated_name_id] = text
                
                # Split text by newlines into paragraph array
                paragraph_list = [p.strip() for p in text.split('\n') if p.strip()]
                
                if not paragraph_list:
                    failed.append(validated_name_id)
                    continue
                
                # Generate embeddings and create paired data structure
                sensor_pairs = []
                for paragraph in paragraph_list:
                    try:
                        embedding = model.encode(paragraph)
                        sensor_pairs.append((paragraph, embedding))
                    except Exception as e:
                        print(f"Error generating embedding for paragraph in {validated_name_id}: {e}")
                        failed.append(validated_name_id)
                        break
                else:
                    # Store paired data: nameId → [(paragraph, embedding), ...]
                    sensor_data_list[validated_name_id] = sensor_pairs
                    created.append(validated_name_id)
                    
            except Exception as e:
                print(f"Error processing sensor {name_id}: {e}")
                failed.append(name_id)
        
        return BulkCreateResponse(
            created=created,
            skipped=skipped,
            failed=failed
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error bulk creating sensors: {str(e)}")

def validate_name_id(name_id: str) -> str:
    """Validate nameId parameter"""
    if not name_id or not name_id.strip():
        raise HTTPException(status_code=400, detail="nameId cannot be empty")
    
    # Remove any potentially problematic characters and limit length
    name_id = name_id.strip()
    if len(name_id) > 100:
        raise HTTPException(status_code=400, detail="nameId is too long (maximum 100 characters)")
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    if not all(c.isalnum() or c in '-_' for c in name_id):
        raise HTTPException(status_code=400, detail="nameId can only contain letters, numbers, hyphens, and underscores")
    
    return name_id

def check_model_availability():
    """Check if the sentence transformer model is available"""
    if model is None:
        error_detail = "Sentence transformer model is not available"
        if model_error:
            error_detail += f": {model_error}"
        raise HTTPException(status_code=503, detail=error_detail)

def check_sensor_exists(name_id: str, operation: str = "access"):
    """Check if a text sensor exists and provide descriptive error messages"""
    if name_id not in sensor_data_list:
        if name_id in text_store:
            # Edge case: text exists but no sensor data (corrupted state)
            raise HTTPException(
                status_code=500, 
                detail=f"Text sensor '{name_id}' is in corrupted state (text exists but no sensor data). Please recreate the sensor."
            )
        else:
            # Normal case: sensor doesn't exist
            available_sensors = list(sensor_data_list.keys())
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

@app.post("/create-text-sensor/{name_id}")
async def create_text_sensor(name_id: str, request: CreateSensorRequest):
    """
    Create a text sensor by splitting text into paragraphs and generating embeddings.
    Stores both paragraph mapping and embedding mapping.
    """
    try:
        # Validate nameId
        name_id = validate_name_id(name_id)
        
        # Check if model is loaded
        check_model_availability()
        
        # Store original text mapping: nameId → full text
        text_store[name_id] = request.text
    
        # Split text by newlines into paragraph array
        paragraph_list = [p.strip() for p in request.text.split('\n') if p.strip()]
        
        if not paragraph_list:
            raise HTTPException(status_code=400, detail="Text must contain at least one non-empty paragraph")
        
        # Generate embeddings and create paired data structure
        sensor_pairs = []
        for paragraph in paragraph_list:
            try:
                embedding = model.encode(paragraph)
                sensor_pairs.append((paragraph, embedding))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error generating embedding for paragraph: {str(e)}")
        
        # Store paired data: nameId → [(paragraph, embedding), ...]
        sensor_data_list[name_id] = sensor_pairs
        
        return {"message": "Text sensor created", "paragraphs_count": len(sensor_pairs)}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating text sensor: {str(e)}")

@app.post("/text-sensor/{name_id}", response_model=SimilarityResponse)
async def check_similarity(name_id: str, request: SimilarityRequest):
    """
    Check semantic similarity against a specific text sensor.
    Parse nameId from URL path, accept text in request body, generate embedding for input text,
    and retrieve stored embeddings for nameId.
    """
    try:
        # Validate nameId
        name_id = validate_name_id(name_id)
        
        # Check if model is loaded
        check_model_availability()
        
        # Check if nameId exists in storage
        check_sensor_exists(name_id, "similarity check")
        
        # Generate embedding for input text using all-MiniLM-L6-v2
        try:
            input_embedding = model.encode(request.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating embedding for input text: {str(e)}")
        
        # Retrieve stored sensor data (paragraph, embedding pairs) for nameId
        sensor_pairs = sensor_data_list[name_id]
        
        if not sensor_pairs:
            raise HTTPException(status_code=404, detail=f"No sensor data found for text sensor '{name_id}'")
        
        # Calculate cosine similarity between input and all stored embeddings
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
        
        # Find the best match (highest similarity score and corresponding paragraph)
        best_match = max(similarity_scores, key=lambda x: x[0])
        highest_score, matched_paragraph = best_match
        
        return {
            "confidence_score": float(highest_score),
            "matched_paragraph": matched_paragraph
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking similarity: {str(e)}")

@app.get("/text-sensors", response_model=SensorListResponse)
async def get_text_sensors():
    """
    Return mapping of nameIds to their text content and count of sensors.
    Format: {"sensors": {"nameId": "text content", ...}, "count": N}
    """
    try:
        # Get all nameIds from the sensor data list (which contains all active sensors)
        # and create mapping of nameId -> text content
        sensors_mapping = {}
        for name_id in sensor_data_list.keys():
            if name_id in text_store:
                sensors_mapping[name_id] = text_store[name_id]
        
        return SensorListResponse(
            sensors=sensors_mapping,
            count=len(sensors_mapping)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving text sensors: {str(e)}")

@app.delete("/text-sensor/{name_id}")
async def delete_text_sensor(name_id: str):
    """
    Remove paragraph mapping and embedding mapping for nameId.
    Return success confirmation.
    """
    try:
        # Validate nameId
        name_id = validate_name_id(name_id)
        
        # Check if nameId exists
        check_sensor_exists(name_id, "deletion")
        
        # Remove text mapping for nameId
        if name_id in text_store:
            del text_store[name_id]
        
        # Remove sensor data (paragraph, embedding pairs) for nameId
        if name_id in sensor_data_list:
            del sensor_data_list[name_id]
        
        return {"message": f"Text sensor '{name_id}' deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting text sensor: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)