<template>
  <div class="mic-stream-container">
    <!-- Video Element -->
    <video
      ref="videoElement"
      autoplay
      playsinline
      muted
      class="webcam-video"
    ></video>

    <!-- Audio Visualizer Overlay (Bottom) -->
    <div class="visualizer-overlay">
      <canvas
        ref="visualizerCanvas"
        class="visualizer-canvas"
      ></canvas>

      <!-- Recording Status Badge -->
      <div v-if="isRecording" class="recording-badge">
        <q-icon name="fiber_manual_record" class="recording-icon" />
        <span>{{ formatDuration(recordingDuration) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Emits
const emit = defineEmits<{
  'audio-chunk': [blob: Blob, duration: number]
}>()

// Refs
const videoElement = ref<HTMLVideoElement | null>(null)
const visualizerCanvas = ref<HTMLCanvasElement | null>(null)

// State
const isRecording = ref(false)
const recordingDuration = ref(0)

// Media streams and recorders
let videoStream: MediaStream | null = null
let mediaRecorder: MediaRecorder | null = null
let audioChunks: Blob[] = []
let recordingTimer: number | null = null
let chunkStartTime = 0

// Audio context for visualization
let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let dataArray: Uint8Array | null = null
let animationFrameId: number | null = null

// Initialize webcam and audio
const initializeMedia = async () => {
  try {
    // Request video and audio
    videoStream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 360 },
        facingMode: 'user'
      },
      audio: {
        channelCount: 1,  // Mono audio
        sampleRate: 16000, // 16kHz sample rate (optimal for speech)
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    })

    // Set video source
    if (videoElement.value) {
      videoElement.value.srcObject = videoStream
    }

    // Setup audio visualization
    setupAudioVisualization(videoStream)

    $q.notify({
      type: 'positive',
      message: 'Camera and microphone ready',
      icon: 'check_circle',
      timeout: 2000
    })
  } catch (error) {
    console.error('Error accessing media devices:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to access camera/microphone',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}

// Setup audio visualization
const setupAudioVisualization = (stream: MediaStream) => {
  try {
    audioContext = new AudioContext()
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 256
    analyser.smoothingTimeConstant = 0.8

    const source = audioContext.createMediaStreamSource(stream)
    source.connect(analyser)

    const bufferLength = analyser.frequencyBinCount
    dataArray = new Uint8Array(bufferLength)

    // Start visualization
    drawVisualizer()
  } catch (error) {
    console.error('Error setting up audio visualization:', error)
  }
}

// Draw visualizer
const drawVisualizer = () => {
  if (!visualizerCanvas.value || !analyser || !dataArray) return

  const canvas = visualizerCanvas.value
  const canvasCtx = canvas.getContext('2d')
  if (!canvasCtx) return

  const WIDTH = canvas.width
  const HEIGHT = canvas.height

  animationFrameId = requestAnimationFrame(drawVisualizer)

  analyser.getByteFrequencyData(dataArray)

  // Create gradient background
  const gradient = canvasCtx.createLinearGradient(0, 0, 0, HEIGHT)
  gradient.addColorStop(0, 'rgba(0, 0, 0, 0.3)')
  gradient.addColorStop(1, 'rgba(0, 0, 0, 0.6)')

  canvasCtx.fillStyle = gradient
  canvasCtx.fillRect(0, 0, WIDTH, HEIGHT)

  const barWidth = (WIDTH / dataArray.length) * 2.5
  let barHeight: number
  let x = 0

  for (let i = 0; i < dataArray.length; i++) {
    barHeight = (dataArray[i] / 255) * HEIGHT * 0.8

    // Create gradient for bars
    const barGradient = canvasCtx.createLinearGradient(0, HEIGHT - barHeight, 0, HEIGHT)

    if (isRecording.value) {
      // Red gradient when recording
      barGradient.addColorStop(0, '#ff5252')
      barGradient.addColorStop(1, '#f44336')
    } else {
      // Blue gradient when not recording
      barGradient.addColorStop(0, '#42a5f5')
      barGradient.addColorStop(1, '#1976d2')
    }

    canvasCtx.fillStyle = barGradient
    canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight)

    x += barWidth + 1
  }
}

// Emit audio chunk
const emitAudioChunk = () => {
  if (audioChunks.length === 0) return

  const blob = new Blob(audioChunks, { type: 'audio/webm' })
  const duration = (Date.now() - chunkStartTime) / 1000

  emit('audio-chunk', blob, duration)

  // Reset for next chunk
  audioChunks = []
  chunkStartTime = Date.now()
}

// Start recording (exposed method)
const start = () => {
  if (!videoStream) {
    console.error('Media stream not ready')
    return
  }

  if (isRecording.value) {
    console.warn('Already recording')
    return
  }

  try {
    // Create audio-only MediaRecorder
    const audioTrack = videoStream.getAudioTracks()[0]
    if (!audioTrack) {
      throw new Error('No audio track available')
    }

    const audioStream = new MediaStream([audioTrack])

    // Determine supported MIME type for audio
    let mimeType = 'audio/webm;codecs=opus'
    if (!MediaRecorder.isTypeSupported(mimeType)) {
      mimeType = 'audio/webm'
    }

    mediaRecorder = new MediaRecorder(audioStream, {
      mimeType,
      audioBitsPerSecond: 128000
    })

    audioChunks = []
    recordingDuration.value = 0
    chunkStartTime = Date.now()

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }

    mediaRecorder.onstop = () => {
      // Emit final chunk if any
      if (audioChunks.length > 0) {
        emitAudioChunk()
      }

      if (recordingTimer) {
        clearInterval(recordingTimer)
        recordingTimer = null
      }
    }

    mediaRecorder.start(100) // Collect data every 100ms
    isRecording.value = true

    // Start duration timer
    recordingTimer = window.setInterval(() => {
      recordingDuration.value++
    }, 1000)

    console.log('Recording started')
  } catch (error) {
    console.error('Error starting recording:', error)
    throw error
  }
}

// Stop recording (exposed method)
const stop = () => {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false

    console.log('Recording stopped')
  }
}

// Format duration
const formatDuration = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// Resize canvas to match container
const resizeCanvas = () => {
  if (visualizerCanvas.value) {
    const container = visualizerCanvas.value.parentElement
    if (container) {
      visualizerCanvas.value.width = container.clientWidth
      visualizerCanvas.value.height = container.clientHeight
    }
  }
}

// Lifecycle hooks
onMounted(async () => {
  await initializeMedia()
  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)
})

onBeforeUnmount(() => {
  // Stop recording if active
  if (isRecording.value) {
    stop()
  }

  // Stop animation frame
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }

  // Stop all media tracks
  if (videoStream) {
    videoStream.getTracks().forEach(track => track.stop())
  }

  // Close audio context
  if (audioContext) {
    audioContext.close()
  }

  // Clear timer
  if (recordingTimer) {
    clearInterval(recordingTimer)
  }

  window.removeEventListener('resize', resizeCanvas)
})

// Expose methods for parent component
defineExpose({
  start,
  stop
})
</script>

<style scoped>
.mic-stream-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background: #000;
  overflow: hidden;
}

.webcam-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.visualizer-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 150px;
  pointer-events: none;
}

.visualizer-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.recording-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(244, 67, 54, 0.9);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 14px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.recording-icon {
  animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .visualizer-overlay {
    height: 100px;
  }

  .controls-overlay {
    bottom: 130px;
  }

  .recording-badge {
    top: 12px;
    right: 12px;
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>
