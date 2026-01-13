<template>
  <div class="mic-stream-container  relative-position" style="width: 360px; height: 360px;">
    <!-- Placeholder Image -->
    <div class="bg-blue-grey-1">
      <img
        src="./skull-man.png"
        alt="Skull Man"
        class="placeholder-image"
      />
    </div>

    <!-- Audio Visualizer -->
    <MicVisualizer :audio-stream="micStream" />

    <!-- VAD Status Indicator -->
    <div v-if="vadEnabled" class="absolute-top-right q-ma-sm">
      <q-badge
        :color="vadState === 'recording' ? 'red' : 'grey'"
      >
        <q-icon
          :name="vadState === 'recording' ? 'mic' : 'hearing'"
          size="xs"
          class="q-mr-xs"
        />
        {{ vadState === 'recording' ? 'Recording' : 'Listening' }}
      </q-badge>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, toRef, nextTick } from 'vue'
import { useQuasar } from 'quasar'
import MicVisualizer from './mic-visualizer.vue'

const $q = useQuasar()

// Props
const props = defineProps<{
  micStream: MediaStream | null
}>()

// Emits
const emit = defineEmits<{
  'recorded-chunk': [blob: Blob, duration: number]
}>()

// State
const isRecording = ref(false)

// VAD state
const vadEnabled = ref(true)
const vadState = ref<'idle' | 'recording'>('idle')
const silenceStartTime = ref<number | null>(null)

// VAD configuration
const VOICE_THRESHOLD = 80
const SILENCE_THRESHOLD = 60
const SILENCE_DURATION = 2500 // 1.5 seconds

// Media streams and recorders
const micStream = toRef(props, 'micStream')
let mediaRecorder: MediaRecorder | null = null
let audioChunks: Blob[] = []
let chunkStartTime = 0

// VAD audio context
let vadAudioContext: AudioContext | null = null
let vadAnalyser: AnalyserNode | null = null
let vadDataArray: Uint8Array | null = null
let vadAnimationFrameId: number | null = null


// Setup VAD
const setupVAD = (stream: MediaStream) => {
  try {
    vadAudioContext = new AudioContext()
    vadAnalyser = vadAudioContext.createAnalyser()
    vadAnalyser.fftSize = 256
    vadAnalyser.smoothingTimeConstant = 0.8

    const source = vadAudioContext.createMediaStreamSource(stream)
    source.connect(vadAnalyser)

    const bufferLength = vadAnalyser.frequencyBinCount
    vadDataArray = new Uint8Array(bufferLength)

    // Start VAD loop
    processVAD()
  } catch (error) {
    console.error('Error setting up VAD:', error)
  }
}

// Calculate audio energy (RMS)
const calculateEnergy = (dataArray: Uint8Array): number => {
  let sum = 0
  for (let i = 0; i < dataArray.length; i++) {
    sum += dataArray[i] * dataArray[i]
  }
  return Math.sqrt(sum / dataArray.length)
}

// VAD processing loop
const processVAD = () => {
  if (!vadAnalyser || !vadDataArray || !vadEnabled.value) {
    vadAnimationFrameId = requestAnimationFrame(processVAD)
    return
  }

  vadAnalyser.getByteFrequencyData(vadDataArray)
  const energy = calculateEnergy(vadDataArray)

  const now = Date.now()

  if (vadState.value === 'idle') {
    // Check if voice detected
    if (energy > VOICE_THRESHOLD) {
      console.log('Voice detected, starting recording. Energy:', energy)
      vadState.value = 'recording'
      silenceStartTime.value = null
      start() // Start recording
    }
  } else if (vadState.value === 'recording') {
    // Check if silence detected
    if (energy < SILENCE_THRESHOLD) {
      if (silenceStartTime.value === null) {
        silenceStartTime.value = now
      } else {
        const silenceDuration = now - silenceStartTime.value
        if (silenceDuration >= SILENCE_DURATION) {
          console.log(`Silence detected for ${silenceDuration/1000}s, stopping recording`)
          vadState.value = 'idle'
          silenceStartTime.value = null
          stop() // Stop recording
        }
      }
    } else {
      // Voice still active, reset silence timer
      silenceStartTime.value = null
    }
  }

  vadAnimationFrameId = requestAnimationFrame(processVAD)
}

// Emit audio chunk
const emitRecordedChunk = () => {
  if (audioChunks.length === 0) return

  const blob = new Blob(audioChunks, { type: 'audio/webm' })
  const duration = (Date.now() - chunkStartTime) / 1000

  emit('recorded-chunk', blob, duration)

  // Reset for next chunk
  audioChunks = []
  chunkStartTime = Date.now()
}

// Start recording (exposed method)
const start = () => {
  if (!micStream.value) {
    console.error('Media stream not ready')
    return
  }

  if (isRecording.value) {
    console.warn('Already recording')
    return
  }

  try {
    // Create audio-only MediaRecorder
    const audioTrack = micStream.value.getAudioTracks()[0]
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
    chunkStartTime = Date.now()

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
      }
    }

    mediaRecorder.onstop = () => {
      // Emit final chunk if any
      if (audioChunks.length > 0) {
        emitRecordedChunk()
      }
    }

    mediaRecorder.start(100) // Collect data every 100ms
    isRecording.value = true

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



// Watch for stream changes and initialize
watch(() => props.micStream, async (newStream) => {
  if (newStream) {
    console.log('Stream received in iv-recorder:', newStream)
    console.log('Audio tracks:', newStream.getAudioTracks())

    // Setup VAD
    if (vadEnabled.value) {
      setupVAD(newStream)
    }
  }
}, { immediate: true })

// Lifecycle hooks
onMounted(() => {
  console.log('iv-recorder mounted')
  console.log('Props micStream:', props.micStream)
})

onBeforeUnmount(() => {
  // Stop recording if active
  if (isRecording.value) {
    stop()
  }

  // Stop VAD
  if (vadAnimationFrameId) {
    cancelAnimationFrame(vadAnimationFrameId)
  }

  if (vadAudioContext) {
    vadAudioContext.close()
  }

  // Note: Stream cleanup is handled by parent component
})

// Expose methods for parent component
defineExpose({
  start,
  stop
})
</script>

<style scoped lang="scss">
.mic-stream-container {
  width: 100%;
  height: 100%;
  background: #000;
  overflow: hidden;
  position: relative;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.person-pic {
  background-image: linear-gradient(50deg, $yellow-1, $red-1);
}
</style>
