<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "index"
})
</script>

<template>
  <a-page>
    <template #stickyTop>
      <a-segment class="shadow-1 bg-grey-1">
        <div class="q-ml-md q-py-sm">
          <a-title st2>Today's Jots</a-title>
          <a-caption>April 19, 2025</a-caption>
        </div>
      </a-segment>
    </template>
    <template #default>
      <a-recording-list />
    </template>
  </a-page>
</template>

<style scoped>

</style>
