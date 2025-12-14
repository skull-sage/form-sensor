<script lang="ts">
import {defineComponent, shallowReactive} from 'vue'
import SettingsStore from '../settings-store';

export default defineComponent({
  name: "input-cam-device",
  props: {
    settingsStore: SettingsStore
  },

  computed: {
    camState(){
      return this.settingsStore.state.cam;
    },

    selectedDevice(){
       return this.camState.deviceList.filter(device => {
         return device.deviceId === this.camState.selectedId;
       })[0];
    }
  },

  methods: {
    setDevice(device) {
      if(device.deviceId === "NONE") {
        this.settingsStore.closeDeviceOnNone(this.camState);
      } else {
        this.settingsStore.tryCamStream(device);
      }
    }
  }
})
</script>

<template>
  <a-nav-item rounded class="bg-brown-1 q-btn--rounded" >
    <q-item-section side>
      <q-icon size="24px" class="text-purple-10" name="r_videocam" />
    </q-item-section>

    <q-item-section>
      <q-item-label class="ellipsis">
        {{ selectedDevice?.label || 'No Camera' }}
      </q-item-label>
    </q-item-section>

    <q-item-section side top v-if="camState.error">
      <q-icon size="24px" class="text-red-9" name="r_warning" />
      <q-tooltip>
        {{camState.error}}
      </q-tooltip>
    </q-item-section>

    <q-menu anchor="center middle" self="center middle" :offset="[0, 0]">
      <q-list v-close-popup style="min-width: 200px">
        <q-item v-for="device in camState.deviceList"
                :key="device.deviceId"
                clickable
                @click="setDevice(device)">
          <q-item-section>
            <q-item-label class="ellipsis">{{ device.label }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </a-nav-item>
</template>

<style scoped>
</style>
