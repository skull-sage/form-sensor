<script setup >
import StageLayout from './stage.layout.vue'
import utilDomToImg from 'dom-to-image'
import {ref, useTemplateRef} from "vue";

const domCanvas = useTemplateRef('dom-canvas')
const recorded = ref([])

const recordDomCanvas = ()=> {
  recorded.value = []
  utilDomToImg.toPng(domCanvas)
    .then(function (dataUrl) {
      let img = new Image();
      img.src = dataUrl;
      recorded.value.push(img)
    })
}


const playAnime = (number)=>{


}
</script>

<template>
  <div class="flex flex-center q-mt-xl">
    <stage-layout style="width: 600px"  >
      <template #input>
        <div class="bg-amber-1 full-height" ref="dom-canvas"></div>
      </template>
      <template #output>
        <canvas></canvas>
      </template>
    </stage-layout>
  </div>
  <div class="flex flex-center q-pa-md">
    <a-btn action primary label="Play Animation" />
    <a-btn action primary label="Play Recorded" />
  </div>

</template>

<style scoped>

</style>
