<script setup lang="ts">
import {defineComponent} from 'vue'
import { SnapType } from './snap-type';
const props = defineProps<SnapType>()

</script>

<template>
  <q-card class="shadow-0 cursor-pointer full-height" >
    <q-img :src="thumbnail" style="height: 160px">
      <a-btn size="32px" flat icon="r_play_circle" class="text-white absolute-center" @click=""/>
      <div class="mdi-text-shadow absolute-bottom-right text-h6 transparent inline-block ">
        5:30s
      </div>
    </q-img>
    <q-card-section>
      <a-title sst weight-bold>{{ title }}</a-title>
      <q-item class="q-mt-sm q-px-none">
        <q-item-section side>
          <q-avatar>
            <img :src="creator_thumb" rounded/>
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <q-item-label >{{ created_by }}</q-item-label>
          <a-text caption>{{ created_at }}</a-text>
        </q-item-section>
        <q-item-section side>
          <div class="text-grey-8 q-gutter-xs">
            <a-btn size="12px" tertiary dense round icon="r_share" />
            <a-btn size="12px" class="gt-xs" tertiary dense round icon="r_delete" />
          </div>
        </q-item-section>
      </q-item>
    </q-card-section>


  </q-card>
</template>

<style scoped>

</style>
