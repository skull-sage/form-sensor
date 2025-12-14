<script setup lang="ts">
import {  shallowReactive, defineProps } from 'vue';
import RecordingStore, { ARecording } from './recording-store';
import { format } from 'quasar';

const props = defineProps({
  recordingId: {
    type: String,
    required: true
  }
})

const state = shallowReactive({
  recording: undefined,
  blobObjUrl: undefined,
  totalSize: '0B',
})

state.recording = RecordingStore.get(props.recordingId)
const blob = new Blob(state.recording.blobList)
state.blobObjUrl = URL.createObjectURL(blob)
state.totalSize = format.humanStorageSize(blob.size)


</script>
<template>
  <a-page class="bg-blue-grey-1">
    <a-section class="q-py-md">
      <a-title >{{ state.recording.title }}</a-title>
      <q-item-label>
            total {{ state.recording.blobList.length }} chunks
            and total size {{ state.totalSize }}
      </q-item-label>

    </a-section>
    <a-section class="q-mt-md">
      <q-responsive :ratio="16/9" style="width: 600px;">
        <video controls class="full-width" preload="metadata"
          :src="state.blobObjUrl"
          />

      </q-responsive>
      <a-btn action primary class="shadow-1 bg-white q-mt-sm" size="small" label="Download"
          :href="state.blobObjUrl" download="recorded-video.webm" />
    </a-section>
  </a-page>
</template>
