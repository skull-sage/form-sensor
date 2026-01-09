"""
Router for the doc-sensor module.
Contains all API endpoints related to CV analysis.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
from .service_cv import CVService
from .service_stt import STTService

from typing import Annotated
from .schemas import (
    CVAnalysisResponse,
    CVDetailResponse,
    CVListResponse,
    DeleteCVResponse
)

# cvService:CVService = CVService() 
sttService:STTService = STTService()

router = APIRouter(prefix="/cv")



def get_service() -> CVService:
    """Get the service instance, raising error if not available"""
    if _service is None:
        raise HTTPException(
            status_code=503,
            detail="CV analysis service is not available"
        )
    return _service


@router.post("/analyze-cv", response_model=CVAnalysisResponse)
async def analyze_cv(file: UploadFile = File(...)):
    """
    Upload and analyze a CV PDF file in one step.
    
    - **file**: PDF file to upload and analyze (max 10MB)
    
    Returns complete CV analysis including:
    - CV ID (for future reference)
    - Basic info (name, email, phone, address, social links)
    - Work experience
    - Skill keywords
    - Education qualifications
    """
    try:
        service = get_service()
        return await service.upload_and_analyze_cv(file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing CV: {str(e)}"
        )


@router.get("/cv/{cv_id}", response_model=CVDetailResponse)
async def get_cv(cv_id: str):
    """
    Get CV details including raw text and analysis if available.
    
    - **cv_id**: UUID of the CV
    
    Returns complete CV data with metadata and analysis results.
    """
    try:
        service = get_service()
        return service.get_cv(cv_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving CV: {str(e)}"
        )


@router.get("/cvs", response_model=CVListResponse)
async def get_all_cvs():
    """
    Get list of all uploaded CVs.
    
    Returns list of CVs with metadata (filename, upload date, analysis status).
    """
    try:
        service = get_service()
        return service.get_all_cvs()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving CVs: {str(e)}"
        )


@router.delete("/cv/{cv_id}", response_model=DeleteCVResponse)
async def delete_cv(cv_id: str):
    """
    Delete a CV and its analysis data.
    
    - **cv_id**: UUID of the CV to delete
    
    Returns confirmation message.
    """
    try:
        service = get_service()
        return service.delete_cv(cv_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting CV: {str(e)}"
        )


@router.post("/analyze-stt")
async def analyze_audio(file: Annotated[bytes, File()]):
    return {text: sttService.transcribe_audioContent(file)}