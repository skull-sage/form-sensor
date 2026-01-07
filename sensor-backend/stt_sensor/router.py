"""
Router for the STT module.
Contains API endpoint for speech-to-text transcription.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional

from .schemas import TranscriptionResponse
from .services import STTService

# Create module router
router = APIRouter(
    prefix="/stt",
    tags=["stt"]
)

# Service instance will be injected
_service: Optional[STTService] = None


def set_service(service: STTService):
    """Set the service instance for this router"""
    global _service
    _service = service


def get_service() -> STTService:
    """Get the service instance, raising error if not available"""
    if _service is None:
        raise HTTPException(
            status_code=503,
            detail="STT service is not available"
        )
    return _service


@router.post("", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...)
):
    """
    Transcribe audio to text using Whisper distil-large-v3.
    
    - **file**: Audio file (wav, mp3, m4a, ogg, flac, webm - max 25MB)
    
    Returns transcribed text with detected language and duration.
    """
    try:
        service = get_service()
        return await service.transcribe_audio(file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error transcribing audio: {str(e)}"
        )
