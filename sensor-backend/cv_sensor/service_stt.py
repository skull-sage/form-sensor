"""
Business logic services for STT operations.
"""

import io
import torch
from fastapi import HTTPException, UploadFile  
import filetype

def load_transcriber():
    """Load Distil-Whisper model and processor."""
    from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
    

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "distil-whisper/distil-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=False, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        torch_dtype=torch_dtype,
        device=device,
    )

    return pipe;


class STTService:
    """Service class for Speech-to-Text operations."""
    
    def __init__(self):
        """
        Initialize the STT service.
        
        Args:
            model: Distil-Whisper model instance
            processor: Distil-Whisper processor instance
        """
        self.transPipe = load_transcriber()
        
    
    async def transcribe_audioContent(self, content: bytes) -> str:
        """
        Transcribe audio content to text.
        
        Args:
            content: Audio content in bytes
            
        Returns:
            str: Transcribed text
        """
        try:
            result = self.transPipe(content)
            txt = result['text']

            return txt
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )

    async def transcribe_audioFile(self, file: UploadFile) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            file: Uploaded audio file / recorded blob
            
        Returns:
            str: Transcribed text
            
        Raises:
            HTTPException: If validation or transcription fails
        """
        
        # Read file content into memory
        file_content = await file.read()

        
        try:
            kind = filetype.guess(file_content)
            
            result = self.transPipe(file_content)
            return result['text']
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )
