<script setup lang="ts">

import {computed, ref} from 'vue'
import {format} from 'quasar'
import SettingsStore from '../settings-store'
import { RecorderState, RuntimeState } from './screen-recorder'
import useRecorder from './use-recorder'

const props = defineProps({
  settingsStore: {
    type: SettingsStore,
    required: true
  },
})

const stream:MediaStream = props.settingsStore.getCombinedStream()

const { state, recorder } = useRecorder(stream)

function togglePause() {
      if (state.runtimeState == RuntimeState.PAUSED)
        recorder.resume();
      else if(state.runtimeState == RuntimeState.RECORDING)
        recorder.pause();
}

function toggleRuntime() {
      if(state.runtimeState == RuntimeState.NOT_STARTED) {
        recorder.start();
      }
      else if(state.runtimeState == RuntimeState.RECORDING){
        recorder.stop();
      }

}


const styleInProgress = computed(()=> {
  if (state.runtimeState == RuntimeState.RECORDING) {
        return "text-orange-9";
      }
      else
        return "text-grey";
})

const stylePasued = computed(()=>{

      if (state.runtimeState == RuntimeState.PAUSED) {
        return "text-warning";
      }
      else
        return "text-grey";

})

const recordedSize = computed(()=> {
   return format.humanStorageSize(state.totalRecordedBytes);
})



</script>

<template>
    <q-item style="width:300px" class="bg-white q-btn--round" >
      <q-item-section side>
        <div>
          <a-btn  tertiary round icon="r_stop_circle"
            @click="toggleRuntime()" :class="[styleInProgress]" />
        <a-btn tertiary round icon="r_pause"
            @click="togglePause()" :class="[stylePasued]" />
        </div>
      </q-item-section>
      <q-item-section>
        <a-text caption>{{ state.chunkList.length }} - {{recordedSize }}</a-text>

      </q-item-section>
      <q-item-section side>
          <!-- <a-btn neutral tertiary round icon="r_replay" /> -->
          <a-btn neutral tertiary round icon="r_delete" />
      </q-item-section>
    </q-item>
</template>

<style scoped>

</style>
