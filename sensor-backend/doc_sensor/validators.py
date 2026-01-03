"""
Validation functions for CV analysis operations.
"""

from fastapi import HTTPException, UploadFile
import re


def validate_pdf_file(file: UploadFile) -> UploadFile:
    """
    Validate that uploaded file is a PDF.
    
    Args:
        file: The uploaded file
        
    Returns:
        UploadFile: The validated file
        
    Raises:
        HTTPException: If file is not a PDF
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Expected PDF, got: {file.filename}"
        )
    
    if not file.content_type or 'pdf' not in file.content_type.lower():
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type. Expected application/pdf, got: {file.content_type}"
        )
    
    return file


def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> None:
    """
    Validate file size is within limits.
    
    Args:
        file_size: Size of file in bytes
        max_size: Maximum allowed size in bytes (default 10MB)
        
    Raises:
        HTTPException: If file exceeds size limit
    """
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        actual_mb = file_size / (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {max_mb:.1f}MB, uploaded: {actual_mb:.1f}MB"
        )


def validate_cv_id(cv_id: str) -> str:
    """
    Validate CV ID format.
    
    Args:
        cv_id: The CV ID to validate
        
    Returns:
        str: The validated CV ID
        
    Raises:
        HTTPException: If CV ID format is invalid
    """
    if not cv_id or not cv_id.strip():
        raise HTTPException(status_code=400, detail="CV ID cannot be empty")
    
    # UUID format validation (basic)
    uuid_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
    if not re.match(uuid_pattern, cv_id.lower()):
        raise HTTPException(
            status_code=400,
            detail="Invalid CV ID format. Expected UUID format"
        )
    
    return cv_id


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid email format
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))
