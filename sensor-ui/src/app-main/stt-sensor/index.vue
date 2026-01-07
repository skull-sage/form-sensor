<template>
  <a-section>
    <div class="q-pa-md">
      <div class="row justify-center">
        <div class="col-12 col-md-8 col-lg-6">
          <q-card flat class="text-center">
            <q-card-section class="q-pt-xl q-pb-lg">
              <div class="text-subtitle1 text-grey-6">Press and hold to speak</div>
            </q-card-section>

            <q-card-section class="q-py-xl">
              <!-- Mic Button with Visualizer -->
              <div class="mic-container">
                <!-- Audio Visualizer Rings -->
                <div v-if="isRecording" class="visualizer-rings">
                  <div
                    v-for="i in 3"
                    :key="i"
                    class="visualizer-ring"
                    :style="{ animationDelay: `${i * 0.2}s` }"
                  ></div>
                </div>

                <!-- Mic Button -->
                <q-btn
                  round
                  size="xl"
                  :color="isRecording ? 'negative' : 'primary'"
                  :icon="isRecording ? 'mic' : 'mic_none'"
                  class="mic-button"
                  :class="{ 'recording': isRecording, 'processing': transcribing }"
                  @mousedown="startRecording"
                  @mouseup="stopRecording"
                  @touchstart="startRecording"
                  @touchend="stopRecording"
                  :disable="transcribing"
                >
                  <q-tooltip v-if="!isRecording && !transcribing">
                    Press and hold to speak
                  </q-tooltip>
                </q-btn>

                <!-- Loading Spinner -->
                <q-spinner-audio
                  v-if="transcribing"
                  color="primary"
                  size="120px"
                  class="loading-spinner"
                />
              </div>

              <!-- Recording Status -->
              <div class="q-mt-lg">
                <div v-if="isRecording" class="text-h6 text-negative">
                  <q-icon name="fiber_manual_record" class="q-mr-xs" />
                  Recording... {{ recordingDuration }}s
                </div>
                <div v-else-if="transcribing" class="text-h6 text-primary">
                  Transcribing...
                </div>
                <div v-else class="text-body2 text-grey-6">
                  Ready to record
                </div>
              </div>
            </q-card-section>

            <!-- Transcription Result -->
            <q-card-section v-if="transcription" class="q-pt-none">
              <q-separator class="q-mb-lg" />

              <div class="transcription-result">
                <div class="text-subtitle2 text-grey-7 q-mb-sm">Transcription:</div>
                <div class="text-h6 text-grey-9 q-mb-md" style="white-space: pre-wrap; line-height: 1.6;">
                  {{ transcription.text }}
                </div>

                <div class="row justify-center q-gutter-sm q-mb-md">
                  <q-chip color="info" text-color="white" icon="language" size="sm">
                    {{ transcription.language }}
                  </q-chip>
                  <q-chip color="positive" text-color="white" icon="schedule" size="sm">
                    {{ transcription.duration }}s
                  </q-chip>
                </div>

                <div class="row justify-center q-gutter-sm">
                  <q-btn
                    flat
                    color="primary"
                    icon="content_copy"
                    label="Copy"
                    @click="copyToClipboard"
                  />
                  <q-btn
                    flat
                    color="grey-7"
                    icon="refresh"
                    label="Clear"
                    @click="clearTranscription"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </a-section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// API base URL
const API_BASE_URL = 'http://localhost:8000'

// Types
interface TranscriptionResponse {
  text: string
  language: string
  duration: number
}

// State
const isRecording = ref(false)
const recordingDuration = ref(0)
const transcribing = ref(false)
const transcription = ref<TranscriptionResponse | null>(null)

// Media recorder
let mediaRecorder: MediaRecorder | null = null
let audioChunks: Blob[] = []
let recordingTimer: number | null = null

// Start recording
const startRecording = async () => {
  if (transcribing.value) return

  try {
    // Request mono audio for voice recording (smaller file size, faster processing)
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,  // Mono audio
        sampleRate: 16000, // 16kHz sample rate (optimal for speech)
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    })

    // Try to use MP3 if supported, fallback to WebM
    let mimeType = 'audio/webm;codecs=opus'
    if (MediaRecorder.isTypeSupported('audio/mp3')) {
      mimeType = 'audio/mp3'
    } else if (MediaRecorder.isTypeSupported('audio/mpeg')) {
      mimeType = 'audio/mpeg'
    }

    const options = {
      mimeType: mimeType,
      audioBitsPerSecond: 128000
    }

    console.log('Using MIME type:', mimeType)

    mediaRecorder = new MediaRecorder(stream, options)
    audioChunks = []
    recordingDuration.value = 0
    transcription.value = null

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data)
        console.log('Audio chunk received:', event.data.size, 'bytes')
      }
    }

    mediaRecorder.onstop = async () => {
      console.log('Recording stopped, total chunks:', audioChunks.length)

      // Create blob with appropriate MIME type
      const blobType = mimeType.includes('mp3') || mimeType.includes('mpeg') ? 'audio/mp3' : 'audio/webm'
      const blob = new Blob(audioChunks, { type: blobType })
      console.log('Final blob size:', blob.size, 'bytes, type:', blobType)

      // Stop all tracks
      stream.getTracks().forEach(track => track.stop())

      // Clear timer
      if (recordingTimer) {
        clearInterval(recordingTimer)
        recordingTimer = null
      }

      // Transcribe immediately
      await transcribeAudio(blob)
    }

    // Start recording with timeslice to collect chunks regularly
    mediaRecorder.start(1000) // Collect chunks every 1 second
    isRecording.value = true

    // Start timer
    recordingTimer = window.setInterval(() => {
      recordingDuration.value++
    }, 1000)

  } catch (error) {
    console.error('Error starting recording:', error)
    $q.notify({
      type: 'negative',
      message: 'Failed to access microphone',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  }
}

// Stop recording
const stopRecording = () => {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false
  }
}

// Transcribe audio
const transcribeAudio = async (blob: Blob) => {
  transcribing.value = true

  try {
    const formData = new FormData()
    // Use appropriate filename based on blob type
    const filename = blob.type.includes('mp3') || blob.type.includes('mpeg')
      ? 'recording.mp3'
      : 'recording.webm'
    formData.append('file', blob, filename)

    console.log('Sending audio for transcription:', filename, blob.size, 'bytes')

    const response = await fetch(`${API_BASE_URL}/stt`, {
      method: 'POST',
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      transcription.value = data

      $q.notify({
        type: 'positive',
        message: 'Transcription completed',
        icon: 'check_circle'
      })
    } else {
      const errorData = await response.json()
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }
  } catch (error) {
    console.error('Error transcribing audio:', error)
    $q.notify({
      type: 'negative',
      message: 'Transcription failed',
      caption: error instanceof Error ? error.message : 'Unknown error'
    })
  } finally {
    transcribing.value = false
  }
}

// Copy to clipboard
const copyToClipboard = () => {
  if (transcription.value) {
    navigator.clipboard.writeText(transcription.value.text)
    $q.notify({
      type: 'positive',
      message: 'Text copied to clipboard',
      icon: 'content_copy'
    })
  }
}

// Clear transcription
const clearTranscription = () => {
  transcription.value = null
  recordingDuration.value = 0
}
</script>

<style scoped>
.mic-container {
  position: relative;
  display: inline-block;
  width: 160px;
  height: 160px;
}

.mic-button {
  width: 120px !important;
  height: 120px !important;
  font-size: 48px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.3s ease;
  z-index: 2;
}

.mic-button:hover {
  transform: translate(-50%, -50%) scale(1.05);
}

.mic-button.recording {
  animation: pulse 1.5s ease-in-out infinite;
}

.mic-button.processing {
  opacity: 0.5;
}

.visualizer-rings {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  z-index: 1;
}

.visualizer-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border: 3px solid #f44336;
  border-radius: 50%;
  opacity: 0;
  animation: ripple 1.5s ease-out infinite;
}

.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
}

.transcription-result {
  max-width: 600px;
  margin: 0 auto;
}

@keyframes pulse {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
  }
}

@keyframes ripple {
  0% {
    width: 120px;
    height: 120px;
    opacity: 0.8;
  }
  100% {
    width: 160px;
    height: 160px;
    opacity: 0;
  }
}
</style>
