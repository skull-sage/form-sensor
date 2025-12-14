<script lang="ts">
import {defineComponent} from 'vue'
import InputMicDevice from "./input-mic-device.vue";
import InputDisplayStream from "./input-display-stream.vue";
import InputCamDevice from "./input-cam-device.vue";
import SettingsStore from "../settings-store";

export default defineComponent({
  name: "recording-init",
  components: {InputCamDevice, InputDisplayStream, InputMicDevice},
  emit: ['start-recording', 'cancel-recording'],
  props: {
    settingsStore : {type: SettingsStore, required: true},
  },
  data() {
    return {
      initProgress: false,
    }
  },
  // async mounted() {
  //   this.initProgress = true;
  //   await this.settingsStore.initDisplayRecording();
  //   this.initProgress = false;
  // },

})
</script>

<template>
  <q-card style="width: 320px">
    <q-card-section>
      <a-text bold>New Recording</a-text>
    </q-card-section>
    <q-separator />
    <q-card-section class="q-py-md q-gutter-md" v-if="!initProgress">
      <input-display-stream :settings-store="settingsStore" />
      <input-cam-device :settings-Store="settingsStore" />
      <input-mic-device :settings-store="settingsStore" />
    </q-card-section>
    <q-separator />
    <q-card-actions align="between" class="q-py-md q-px-md"  >
      <q-spinner v-if="initProgress" />
      <a-btn v-else primary action rounded icon="r_fiber_smart_record" label="Start"
             style="padding-left: 8px; padding-right: 12px;"
             @click="$emit('start-recording');" />
      <a-btn action tertiary label="Cancel" @click="$emit('cancel-recording')" />
      </q-card-actions>
  </q-card>
</template>

<style scoped>

</style>
