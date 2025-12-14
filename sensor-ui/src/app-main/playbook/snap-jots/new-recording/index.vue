<script lang="ts">
import {defineComponent, markRaw} from 'vue'

import SettingsStore from "./settings-store"
import RecordingInit from './recording-init/index.vue'
import RecordingRuntime from './recording-runtime/index.vue'



export default defineComponent({
  name: "new-recording",
  components: {RecordingInit, RecordingRuntime},
  data(){
    return {
      initDialogVisible: false,
      runtimeDialogVisible: false,
      settingsStore : undefined,
      initProgress: false,

    }
  },
  created(){

  },


  methods: {
    async initRecording(){
      this.settingsStore  = markRaw(new SettingsStore());
      this.initProgress = true;
      await this.settingsStore.initDisplayRecording();
      this.initProgress = false;
      this.initDialogVisible = true;
    },
    cancelRecording(){
      this.initDialogVisible = false;
      this.settingsStore.close();
      this.settingsStore = undefined;
    },
    startRecording(){
      this.initDialogVisible = false;
      this.runtimeDialogVisible = true;
    },
    onRecordingComplete(jotId: string){
      this.runtimeDialogVisible = false;
      this.settingsStore.close();
      this.settingsStore = undefined;
    }
  }

})
</script>

<template>
  <a-btn action primary icon="r_add" @click="initRecording()" :loading="initProgress" >
    <div>Create a new jot</div>
    <!--init recording dialog-->
    <q-dialog v-model="initDialogVisible" >
      <recording-init :settings-store="settingsStore"
                      @start-recording="startRecording"
                      @cancel-recording="cancelRecording" />
    </q-dialog>
    <q-dialog v-model="runtimeDialogVisible" position="bottom" persistent >
      <recording-runtime :settings-store="settingsStore" v-if="runtimeDialogVisible"
                         @cancel-recording="cancelRecording"
                         @stop-recording="onRecordingComplete" />
    </q-dialog>

  </a-btn>
</template>

<style scoped>
    .shape-capsule {
      border-radius: 1rem;
    }
</style>
