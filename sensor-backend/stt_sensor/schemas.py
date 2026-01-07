"""
Pydantic schemas for STT module.
"""

from pydantic import BaseModel, Field


class TranscriptionResponse(BaseModel):
    """Response for audio transcription."""
    text: str = Field(description="Transcribed text from audio")
    language: str = Field(description="Detected language")
    duration: float = Field(description="Audio duration in seconds")
