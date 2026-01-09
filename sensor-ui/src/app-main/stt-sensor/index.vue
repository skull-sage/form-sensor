<template>
<div class="fullscreen flex flex-center iv-container">
  <div style="width: 1080px;" class="q-pa-xl">
    <div class="text-bold text-h5 q-mt-md">
      Rashed's Interview

    </div>
    <div class="row full-width">
      <div class="col-md-6">
        <div ref="qBox"></div>
      </div>
      <div class="col-md-6">
        <MicStream ref="micStream" class="rounded-borders shadow-8"
            @recorded-chunk="handleRecordedChunk" />

        </div>
    </div>
  </div>

</div>
</template>
<script setup lang="ts">
import MicStream from './mic-stream.vue';
import { ref } from 'vue';

const micStream = ref<InstanceType<typeof MicStream> | null>(null)

const handleRecordedChunk = (blob: Blob, duration: number) => {
  console.log('Recorded chunk:', blob, duration)
}

const startRecording = () => {
  if (micStream.value) {
    micStream.value.start()
  }
}

const stopRecording = () => {
  if (micStream.value) {
    micStream.value.stop()
  }
}
</script>
<style scoped lang="scss">
  .iv-container {
    background-image: linear-gradient(to bottom, $blue-grey-1, $red-1);
  }
</style>
