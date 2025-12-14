<script lang="ts">
import {defineComponent, shallowReactive} from 'vue'
import SettingsStore from "../settings-store.ts"

export default defineComponent({
  name: "input-display-stream",
  props: {
    settingsStore: SettingsStore
  }
})
</script>

<template>
  <a-nav-item class="bg-blue-grey-1 q-btn--rounded">
    <q-item-section side><q-icon size="24px" class="text-purple-9" name="r_fullscreen" /></q-item-section>
    <q-item-section>
      <q-item-label >Full Screen</q-item-label>
    </q-item-section>
  </a-nav-item>
</template>

<style scoped>

</style>
