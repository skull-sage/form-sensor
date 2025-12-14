<script setup lang="ts">
import ARecordedItem from './a-recorded-item.vue'
import NewRecording from './new-recording/index.vue'
import {defineComponent} from 'vue'
import { sample_list } from './sample-data'

</script>

<template>
  <a-page class="bg-blue-grey-1">
    <template #stickyTop>
      <a-segment class="shadow-1 bg-grey-1">
        <div class=" q-py-sm">
          <div class="text-bold title-h3">Video Jots at work</div>
          <div class="text-grey-8"> 9 Recording</div>
        </div>
      </a-segment>
    </template>
    <template #default>
      <a-section class="q-py-lg">
        <new-recording />

        <div class="row q-col-gutter-xl q-pt-md">
          <div class="col-xs-12 col-sm-6 col-md-4" v-for="(sample, idx) in sample_list" :key="idx">
            <a-recorded-item v-bind="sample"  />
          </div>
        </div>
      </a-section>
    </template>
  </a-page>
</template>

<style scoped>

</style>
