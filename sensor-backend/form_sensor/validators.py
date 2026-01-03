"""
Validation functions for the semantic sensor API.
All input validation logic is centralized here for easy discovery and maintenance.
"""

from fastapi import HTTPException
from typing import List


def validate_name_id(name_id: str) -> str:
    """
    Validate nameId parameter for sensor operations.
    
    Args:
        name_id: The nameId to validate
        
    Returns:
        str: The validated and cleaned nameId
        
    Raises:
        HTTPException: If validation fails
    """
    if not name_id or not name_id.strip():
        raise HTTPException(status_code=400, detail="nameId cannot be empty")
    
    # Remove any potentially problematic characters and limit length
    name_id = name_id.strip()
    if len(name_id) > 100:
        raise HTTPException(status_code=400, detail="nameId is too long (maximum 100 characters)")
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    if not all(c.isalnum() or c in '-_' for c in name_id):
        raise HTTPException(
            status_code=400, 
            detail="nameId can only contain letters, numbers, hyphens, and underscores"
        )
    
    return name_id


def validate_text_content(text: str, max_length: int = 10000, field_name: str = "text") -> str:
    """
    Validate text content for sensor operations.
    
    Args:
        text: The text content to validate
        max_length: Maximum allowed length for the text
        field_name: Name of the field being validated (for error messages)
        
    Returns:
        str: The validated and cleaned text
        
    Raises:
        HTTPException: If validation fails
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail=f"{field_name} cannot be empty or contain only whitespace")
    
    text = text.strip()
    if len(text) > max_length:
        raise HTTPException(
            status_code=400, 
            detail=f"{field_name} is too long (maximum {max_length:,} characters)"
        )
    
    return text


def validate_paragraphs(paragraphs: List[str]) -> List[str]:
    """
    Validate that paragraphs list is not empty and contains valid content.
    
    Args:
        paragraphs: List of paragraph strings
        
    Returns:
        List[str]: The validated paragraphs
        
    Raises:
        HTTPException: If validation fails
    """
    if not paragraphs:
        raise HTTPException(status_code=400, detail="Text must contain at least one non-empty paragraph")
    
    # Filter out any empty paragraphs that might have slipped through
    valid_paragraphs = [p for p in paragraphs if p.strip()]
    
    if not valid_paragraphs:
        raise HTTPException(status_code=400, detail="Text must contain at least one non-empty paragraph")
    
    return valid_paragraphs


def validate_bulk_sensors(sensors_dict: dict) -> dict:
    """
    Validate bulk sensor creation data.
    
    Args:
        sensors_dict: Dictionary of nameId -> text mappings
        
    Returns:
        dict: The validated sensors dictionary
        
    Raises:
        HTTPException: If validation fails
    """
    if not sensors_dict:
        raise HTTPException(status_code=400, detail="No sensors provided for bulk creation")
    
    if len(sensors_dict) > 50:  # Reasonable limit for bulk operations
        raise HTTPException(status_code=400, detail="Too many sensors for bulk creation (maximum 50)")
    
    validated_sensors = {}
    
    for name_id, text in sensors_dict.items():
        try:
            validated_name_id = validate_name_id(name_id)
            validated_text = validate_text_content(text, max_length=10000, field_name=f"text for sensor '{name_id}'")
            validated_sensors[validated_name_id] = validated_text
        except HTTPException as e:
            # Re-raise with context about which sensor failed
            raise HTTPException(
                status_code=e.status_code,
                detail=f"Validation failed for sensor '{name_id}': {e.detail}"
            )
    
    return validated_sensors