"""
Router for the form-ocr module.
Contains all API endpoints related to form OCR processing.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional

from .schemas import (
    FormProcessResponse,
    FormDetailResponse,
    FormListResponse,
    DeleteFormResponse,
    FormImagesResponse,
    OCROptions
)
from .services import FormOCRService

# Create module router
router = APIRouter(
    prefix="/form-ocr",
    tags=["form-ocr"]
)

# Service instance will be injected
_service: Optional[FormOCRService] = None


def set_service(service: FormOCRService):
    """Set the service instance for this router"""
    global _service
    _service = service


def get_service() -> FormOCRService:
    """Get the service instance, raising error if not available"""
    if _service is None:
        raise HTTPException(
            status_code=503,
            detail="Form OCR service is not available"
        )
    return _service


@router.post("/process-form", response_model=FormProcessResponse)
async def process_form(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
    use_gpu: bool = Form(default=False),
    enable_correction: bool = Form(default=True),
    confidence_threshold: float = Form(default=0.5),
    enable_segment_detection: bool = Form(default=True)
):
    """
    Upload and process a form PDF in one step.
    
    - **file**: PDF file to upload and process (max 20MB)
    - **language**: OCR language code (default: "en")
    - **use_gpu**: Enable GPU acceleration (default: False)
    - **enable_correction**: Apply perspective correction (default: True)
    - **confidence_threshold**: Minimum confidence score (0-1, default: 0.5)
    - **enable_segment_detection**: Enable form segment detection (default: True)
    
    Returns complete form processing results including:
    - Form ID (for future reference)
    - Page count and processing time
    - Original and corrected images (base64)
    - Extracted text regions with bounding boxes
    - Detected form fields (label-value pairs)
    """
    try:
        # Create OCR options
        options = OCROptions(
            language=language,
            use_gpu=use_gpu,
            enable_correction=enable_correction,
            confidence_threshold=confidence_threshold,
            enable_segment_detection=enable_segment_detection
        )
        
        service = get_service()
        return await service.process_form(file, options)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing form: {str(e)}"
        )


@router.get("/form/{form_id}", response_model=FormDetailResponse)
async def get_form(form_id: str):
    """
    Get form details including processing results.
    
    - **form_id**: UUID of the form
    
    Returns complete form data with metadata and processing results.
    """
    try:
        service = get_service()
        return service.get_form(form_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving form: {str(e)}"
        )


@router.get("/forms", response_model=FormListResponse)
async def get_all_forms():
    """
    Get list of all processed forms.
    
    Returns list of forms with metadata (filename, upload date, processing status).
    """
    try:
        service = get_service()
        return service.get_all_forms()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving forms: {str(e)}"
        )


@router.delete("/form/{form_id}", response_model=DeleteFormResponse)
async def delete_form(form_id: str):
    """
    Delete a form and its processing results.
    
    - **form_id**: UUID of the form to delete
    
    Returns confirmation message.
    """
    try:
        service = get_service()
        return service.delete_form(form_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting form: {str(e)}"
        )


@router.get("/form/{form_id}/images", response_model=FormImagesResponse)
async def get_form_images(form_id: str):
    """
    Get original and corrected images for a form.
    
    - **form_id**: UUID of the form
    
    Returns images as base64 strings for each page.
    """
    try:
        service = get_service()
        return service.get_form_images(form_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving form images: {str(e)}"
        )
