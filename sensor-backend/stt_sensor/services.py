"""
Business logic services for STT operations.
"""

import tempfile
import os
import torch
from fastapi import HTTPException, UploadFile
from .validators import validate_audio_file, validate_file_size
from .schemas import TranscriptionResponse


class STTService:
    """Service class for Speech-to-Text operations."""
    
    def __init__(self, model, processor):
        """
        Initialize the STT service.
        
        Args:
            model: Distil-Whisper model instance
            processor: Distil-Whisper processor instance
        """
        self.model = model
        self.processor = processor
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    async def transcribe_audio(self, file: UploadFile) -> TranscriptionResponse:
        """
        Transcribe audio file to text.
        
        Args:
            file: Uploaded audio file
            
        Returns:
            TranscriptionResponse: Transcription result
            
        Raises:
            HTTPException: If validation or transcription fails
        """
        # Validate file
        validate_audio_file(file)
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size (25MB max)
        validate_file_size(len(file_content))
        
        # Save to temporary file
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name
            
            # Load audio using librosa or torchaudio
            import librosa
            audio, sample_rate = librosa.load(temp_path, sr=16000)
            
            # Calculate duration
            duration = len(audio) / sample_rate
            
            # Process audio
            inputs = self.processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate transcription
            with torch.no_grad():
                predicted_ids = self.model.generate(inputs["input_features"])
            
            # Decode transcription
            transcription = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]
            
            # Clean up temp file
            os.unlink(temp_path)
            
            # Distil-Whisper doesn't return language, default to English
            # You can add language detection if needed
            language = "en"
            
            return TranscriptionResponse(
                text=transcription.strip(),
                language=language,
                duration=round(duration, 2)
            )
            
        except Exception as e:
            # Clean up temp file if it exists
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )
