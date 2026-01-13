<template>
  <div class="text-center q-pa-xl">
    <div class="text-h3 text-bold text-grey-6">
      Welcome Mr. Skull
    </div>
    <div class="text-h6 text-blue-grey-8">
      We hope you are ready to start the interview
    </div>
    <q-btn
      label="I am ready"
      icon-right="arrow_forward"
      color="primary"
      class="q-mt-md" rounded
      @click="handleReady"
      :loading="isInitializing"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Emits
const emit = defineEmits<{
  'stream-ready': [stream: MediaStream]
}>()

// State
const isInitializing = ref(false)

// Initialize media stream and emit
const handleReady = async () => {
  isInitializing.value = true

  try {
    // Request video and audio access
    const stream = await navigator.mediaDevices.getUserMedia({
      // video: {
      //   width: { ideal: 360 },
      //   height: { ideal: 360 },
      //   facingMode: 'user'
      // },
      audio: {
        channelCount: 1,  // Mono audio
        sampleRate: 16000, // 16kHz sample rate (optimal for speech)
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      }
    })

    // Emit the stream to parent
    emit('stream-ready', stream)

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
      caption: error instanceof Error ? error.message : 'Unknown error',
      timeout: 5000
    })
  } finally {
    isInitializing.value = false
  }
}
</script>
