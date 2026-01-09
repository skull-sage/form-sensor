<template>
  <div class="visualizer-canvas absolute-bottom">
    <canvas ref="visualizerCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

// Props
const props = defineProps<{
  audioStream: MediaStream | null
}>()

// Refs
const visualizerCanvas = ref<HTMLCanvasElement | null>(null)

// Audio context for visualization
let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let dataArray: Uint8Array<ArrayBuffer> | null = null
let animationFrameId: number | null = null

// Setup audio visualization
const setupAudioVisualization = (stream: MediaStream) => {
  try {
    // Clean up existing context if any
    cleanupAudioContext()

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

  // Clear canvas with transparent background
  canvasCtx.clearRect(0, 0, WIDTH, HEIGHT)

  const barWidth = (WIDTH / dataArray.length) * 2.5
  let barHeight: number
  let x = 0

  // Create gradient for bars
  const grd = canvasCtx.createLinearGradient(0, 0, 0, canvas.height)
  grd.addColorStop(1, "rgba(255, 255, 255, 0.4)")   // Bottom: white
  grd.addColorStop(0.3, "rgba(61, 224, 107, 0.6)") // Top: green
  canvasCtx.fillStyle = grd

  for (let i = 0; i < dataArray.length; i++) {
    barHeight = (dataArray[i] / 255) * HEIGHT * 0.8

    canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight)

    x += barWidth + 1
  }
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

// Clean up audio context
const cleanupAudioContext = () => {
  // Stop animation frame
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
    animationFrameId = null
  }

  // Close audio context
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }

  analyser = null
  dataArray = null
}

// Watch for audio stream changes
watch(() => props.audioStream, (newStream) => {
  if (newStream) {
    setupAudioVisualization(newStream)
  } else {
    cleanupAudioContext()
  }
})

// Lifecycle hooks
onMounted(() => {
  resizeCanvas()
  window.addEventListener('resize', resizeCanvas)

  // Initialize if stream is already provided
  if (props.audioStream) {
    setupAudioVisualization(props.audioStream)
  }
})

onBeforeUnmount(() => {
  cleanupAudioContext()
  window.removeEventListener('resize', resizeCanvas)
})
</script>

<style scoped>
.visualizer-canvas {
  width: 100%;
  height: 100%;
  display: block;
  pointer-events: none;
}

.visualizer-canvas canvas {
  width: 100%;
  height: 100%;
}
</style>
