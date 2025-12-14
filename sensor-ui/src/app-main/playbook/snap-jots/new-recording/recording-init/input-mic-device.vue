<script lang="ts">
import {defineComponent, shallowReactive} from 'vue'
import SettingsStore from "../settings-store"

export default defineComponent({
  name: "input-mic-device",
  props: {
    settingsStore : SettingsStore,
  },


  computed: {

    micState(){
      return this.settingsStore.state.mic;
    },

    selectedDevice(){
      return this.micState.deviceList.filter(device => {
        return device.deviceId === this.micState.selectedId;
      })[0]

    }

  },

  methods: {
    setDevice(device){
      if(device.deviceId === "NONE"){
        this.settingsStore.closeDeviceOnNone(this.micState);
      }
      else {
        this.settingsStore.tryMicStream(device);
      }
    }
  }

})
</script>

<template>
  <a-nav-item class="bg-brown-1 q-btn--rounded" >
    <q-item-section side>
      <q-icon size="24px" class="text-purple-9" name="r_mic" />
    </q-item-section>
    <q-item-section>
      <q-item-label class="ellipsis">{{ selectedDevice.label }}</q-item-label>
    </q-item-section>
    <q-item-section side top v-if="micState.error">
      <q-icon size="24px" class="text-red-9" name="r_warning" />
      <q-tooltip>
          {{micState.error}}
        </q-tooltip>
    </q-item-section>
    <q-menu  anchor="center middle" self="center middle" :offset="[0, 0]">
        <q-list v-close-popup style="min-width: 200px">
          <q-item v-for="device in micState.deviceList"
                :key="device.deviceId"
                clickable
                @click="setDevice(device)">
          <q-item-section>
            <q-item-label>{{ device.label }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </a-nav-item>
</template>

<style scoped>

</style>
