# STT Sensor Module

Speech-to-Text transcription using Distil-Whisper distil-large-v3 from Hugging Face.

## Features

- Audio transcription from multiple formats (wav, mp3, m4a, ogg, flac, webm)
- Automatic language detection (English optimized)
- Audio duration calculation
- GPU acceleration support
- Max file size: 25MB

## Installation

```bash
pip install transformers torch librosa accelerate
```

## Model

Uses [distil-whisper/distil-large-v3](https://huggingface.co/distil-whisper/distil-large-v3) from Hugging Face:
- 6x faster than Whisper large-v3
- 49% smaller model size
- Maintains high accuracy
- Optimized for English transcription

## API Endpoint

### POST /stt

Transcribe audio to text.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (audio file)

**Response:**
```json
{
  "text": "Transcribed text from the audio",
  "language": "en",
  "duration": 12.5
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/stt \
  -F "file=@recording.wav"
```

**Example (Python):**
```python
import requests

with open("recording.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8000/stt",
        files={"file": f}
    )
    
result = response.json()
print(f"Transcription: {result['text']}")
print(f"Language: {result['language']}")
print(f"Duration: {result['duration']}s")
```

**Example (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('file', audioBlob, 'recording.wav');

const response = await fetch('http://localhost:8000/stt', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Transcription:', result.text);
console.log('Language:', result.language);
console.log('Duration:', result.duration);
```

## Error Handling

- **400 Bad Request**: Invalid file format or missing file
- **413 Payload Too Large**: File exceeds 25MB
- **500 Internal Server Error**: Transcription failed
- **503 Service Unavailable**: Distil-Whisper model not loaded

## Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3)
- M4A (.m4a)
- OGG (.ogg)
- FLAC (.flac)
- WebM (.webm)

## Performance

- **CPU**: ~5-10 seconds for 30-second audio
- **GPU**: ~1-2 seconds for 30-second audio
- Model automatically uses GPU if available (CUDA)
