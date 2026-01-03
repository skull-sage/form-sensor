"""
Input validation functions for Form OCR module.
"""

from fastapi import HTTPException, UploadFile


def validate_pdf_file(file: UploadFile) -> None:
    """
    Validate uploaded PDF file.
    
    Args:
        file: Uploaded file
        
    Raises:
        HTTPException: If validation fails
    """
    # Check if file exists
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )
    
    # Check file extension
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Check content type
    if file.content_type and file.content_type != 'application/pdf':
        raise HTTPException(
            status_code=400,
            detail="Invalid content type. Expected application/pdf"
        )


def validate_file_size(file_size: int, max_size: int = 20 * 1024 * 1024) -> None:
    """
    Validate file size.
    
    Args:
        file_size: File size in bytes
        max_size: Maximum allowed size in bytes (default: 20MB)
        
    Raises:
        HTTPException: If file is too large
    """
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {max_mb}MB"
        )


def validate_form_id(form_id: str) -> str:
    """
    Validate form ID format.
    
    Args:
        form_id: Form identifier
        
    Returns:
        str: Validated form ID
        
    Raises:
        HTTPException: If form ID is invalid
    """
    if not form_id or not form_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Form ID is required"
        )
    
    return form_id.strip()


def validate_ocr_options(options: dict) -> dict:
    """
    Validate OCR options.
    
    Args:
        options: OCR options dictionary
        
    Returns:
        dict: Validated options
        
    Raises:
        HTTPException: If options are invalid
    """
    # Validate language
    if 'language' in options:
        valid_languages = ['en', 'ch', 'fr', 'german', 'korean', 'japan']
        if options['language'] not in valid_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid language. Must be one of: {', '.join(valid_languages)}"
            )
    
    # Validate confidence threshold
    if 'confidence_threshold' in options:
        threshold = options['confidence_threshold']
        if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 1:
            raise HTTPException(
                status_code=400,
                detail="Confidence threshold must be between 0 and 1"
            )
    
    return options
