# STT Sensor Frontend

Speech-to-Text transcription interface with audio recording and file upload.

## Features

### Audio Recording
- **Record Audio**: Click "Start Recording" to record from microphone
- **Live Timer**: Shows recording duration in real-time
- **Audio Playback**: Preview recorded audio before transcription
- **Re-record**: Easy reset to record again

### File Upload
- **Drag & Drop**: Upload audio files directly
- **Format Support**: WAV, MP3, M4A, OGG, FLAC, WebM
- **Size Limit**: Max 25MB

### Transcription
- **One-Click**: Transcribe recorded or uploaded audio
- **Real-time Feedback**: Loading indicator during processing
- **Results Display**: Shows transcribed text, language, and duration
- **Copy to Clipboard**: Quick copy button for transcribed text

## Components

### index.vue
Main component with:
- Audio recording controls
- File upload interface
- Transcription display
- Copy functionality

### route-config.ts
Route configuration:
- Path: `/stt`
- Name: `stt`
- Icon: `mic`

## Usage

### Recording Audio
1. Click "Start Recording"
2. Speak into microphone
3. Click "Stop Recording"
4. Preview audio (optional)
5. Click "Transcribe Audio"

### Uploading Audio
1. Click "Select audio file" or drag & drop
2. Choose audio file from device
3. Click "Transcribe Audio"

### Viewing Results
- Transcribed text appears in a card
- Language and duration shown as chips
- Click "Copy Text" to copy to clipboard

## API Integration

Calls `POST /stt` endpoint:
```typescript
const formData = new FormData()
formData.append('file', audioFile)

const response = await fetch('http://localhost:8000/stt', {
  method: 'POST',
  body: formData
})

const result = await response.json()
// { text: string, language: string, duration: number }
```

## Browser Compatibility

Requires:
- **MediaRecorder API**: For audio recording
- **getUserMedia API**: For microphone access
- **Clipboard API**: For copy functionality

Supported browsers:
- Chrome/Edge 49+
- Firefox 25+
- Safari 14.1+

## Permissions

Requires microphone permission for recording:
- Browser will prompt on first recording attempt
- User must grant permission to record audio

## Error Handling

- Microphone access denied → Shows error notification
- File too large → Backend returns 413 error
- Invalid format → Backend returns 400 error
- Transcription failed → Shows error with details
