"""
Business logic services for STT operations.
"""

import io
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
        
        # Read file content into memory
        file_content = await file.read()
        
        # Validate file size (25MB max)
        validate_file_size(len(file_content))
        
        try:
            print(f"Processing audio file: {file.filename}, size: {len(file_content)} bytes")
            
            # Create buffer from uploaded audio
            audio_buffer = io.BytesIO(file_content)
            audio_buffer.name = file.filename or 'audio.mp3'
            
            # Load audio with torchaudio (simpler than librosa)
            import torchaudio
            
            # Load audio from buffer
            waveform, sample_rate = torchaudio.load(audio_buffer)
            
            # Convert to mono if stereo
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            
            # Resample to 16kHz if needed
            if sample_rate != 16000:
                resampler = torchaudio.transforms.Resample(sample_rate, 16000)
                waveform = resampler(waveform)
                sample_rate = 16000
            
            # Convert to numpy array and flatten
            audio = waveform.squeeze().numpy()
            
            # Calculate duration
            duration = len(audio) / sample_rate
            print(f"Audio duration: {duration:.2f} seconds, samples: {len(audio)}")
            
            # Process audio with Whisper processor
            inputs = self.processor(
                audio,
                sampling_rate=16000,
                return_tensors="pt"
            ).to(self.device)
            
            print(f"Input features shape: {inputs['input_features'].shape}")
            
            # Generate transcription
            max_new_tokens = 448 if duration <= 30 else int(duration * 15)
            print(f"Using max_new_tokens: {max_new_tokens}")
            
            with torch.no_grad():
                predicted_ids = self.model.generate(
                    inputs["input_features"],
                    max_new_tokens=max_new_tokens
                )
            
            # Decode transcription
            transcription = self.processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True
            )[0]
            
            print(f"Transcription: {transcription}")
            
            return TranscriptionResponse(
                text=transcription.strip(),
                language="en",
                duration=round(duration, 2)
            )
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )
