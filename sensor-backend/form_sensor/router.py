"""
Router for the form-sensor module.
Contains all API endpoints related to text sensor management and similarity checking.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from .schemas import (
    CreateSensorRequest, SimilarityRequest, SimilarityResponse,
    BulkCreateRequest, BulkCreateResponse, SensorListResponse,
    CreateSensorResponse, DeleteSensorResponse
)
from .services import SensorService

# Create module router
router = APIRouter(
    prefix="/form-sensor",
    tags=["form-sensor"]
)

# Service instance will be injected
_service: Optional[SensorService] = None


def set_service(service: SensorService):
    """Set the service instance for this router"""
    global _service
    _service = service


def get_service() -> SensorService:
    """Get the service instance, raising error if not available"""
    if _service is None:
        raise HTTPException(
            status_code=503, 
            detail="Form sensor service is not available - model not loaded"
        )
    return _service


@router.post("/bulk-create-sensors", response_model=BulkCreateResponse)
async def bulk_create_sensors(request: BulkCreateRequest):
    """Bulk create text sensors from browser storage."""
    try:
        service = get_service()
        return service.bulk_create_sensors(request.sensors)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error bulk creating sensors: {str(e)}"
        )


@router.post("/create-text-sensor/{name_id}", response_model=CreateSensorResponse)
async def create_text_sensor(name_id: str, request: CreateSensorRequest):
    """Create a text sensor by splitting text into paragraphs and generating embeddings."""
    try:
        service = get_service()
        return service.create_sensor(name_id, request.text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating text sensor: {str(e)}"
        )


@router.post("/text-sensor/{name_id}", response_model=SimilarityResponse)
async def check_similarity(name_id: str, request: SimilarityRequest):
    """Check semantic similarity against a specific text sensor."""
    try:
        service = get_service()
        result = service.calculate_similarity(request.text, name_id)
        return SimilarityResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error checking similarity: {str(e)}"
        )


@router.get("/text-sensors", response_model=SensorListResponse)
async def get_text_sensors():
    """Return mapping of nameIds to their text content and count of sensors."""
    try:
        service = get_service()
        result = service.get_all_sensors()
        return SensorListResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving text sensors: {str(e)}"
        )


@router.delete("/text-sensor/{name_id}", response_model=DeleteSensorResponse)
async def delete_text_sensor(name_id: str):
    """Remove text sensor and return success confirmation."""
    try:
        service = get_service()
        result = service.delete_sensor(name_id)
        return DeleteSensorResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error deleting text sensor: {str(e)}"
        )
