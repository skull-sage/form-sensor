<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "flex-apart"
})
</script>

<template>
  <div class="flex justify-between">
    <div><slot name="left"></slot></div>
    <div><slot name="right"></slot></div>
  </div>
</template>

<style scoped>

</style>
