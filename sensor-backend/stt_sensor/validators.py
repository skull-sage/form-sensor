"""
Input validation functions for STT module.
"""

from fastapi import HTTPException, UploadFile


def validate_audio_file(file: UploadFile) -> None:
    """
    Validate uploaded audio file.
    
    Args:
        file: Uploaded file
        
    Raises:
        HTTPException: If validation fails
    """
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )
    
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )
    
    # Accept common audio formats
    valid_extensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac', '.webm']
    if not any(file.filename.lower().endswith(ext) for ext in valid_extensions):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid audio format. Supported: {', '.join(valid_extensions)}"
        )


def validate_file_size(file_size: int, max_size: int = 25 * 1024 * 1024) -> None:
    """
    Validate file size.
    
    Args:
        file_size: File size in bytes
        max_size: Maximum allowed size in bytes (default: 25MB)
        
    Raises:
        HTTPException: If file is too large
    """
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {max_mb}MB"
        )
