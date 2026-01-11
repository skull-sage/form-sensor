<template>
<div class="fullscreen flex flex-center" id="iv-container">
  <div class="text-center q-pa-xl" v-if="!ivStarted">
    <div class="text-h3 text-bold text-grey-6">
      Welcome Rashed
    </div>
    <div class="text-h6 text-blue-grey-8 ">
      We hope you are ready to start the interview
    </div>
    <q-btn label="I am ready" color="primary" class="q-mt-md" @click="ivStarted = true" />
  </div>
  <div style="width: 1080px;" class="q-pa-xl" v-else>
    <div class="text-bold text-h5 q-mt-md q-mb-lg">
      Rashed's Interview
    </div>
    <div class="row full-width">
      <div class="col-md-6 q-mt-lg">
        <SmartTxt :key="currentQ.id" :audio-file="roboBeep">{{ currentQ.query }}</SmartTxt>
      </div>
      <div class="col-md-6 justify-center">
        <MicStream ref="micStream" class="rounded-borders shadow-8"
            @recorded-chunk="handleRecordedChunk" />

        </div>
    </div>
  </div>

</div>
</template>
<script setup lang="ts">
import MicStream from './mic-stream.vue';
import { reactive, ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { animate } from 'animejs';
import cvAPI from './cv-api';
import SmartTxt from './smart-txt.vue';
import roboBeep from './robo-beep-30.wav';



const ivStarted = ref(false)
const currentQ = computed(() => cvAPI.currentQ())


const handleRecordedChunk = async (blob: Blob, duration: number) => {
  let {text:answer, score} = await cvAPI.analyzeAudio(blob, currentQ.value.query);

}


// Animation instance for cleanup
let angAnim: any = null;
onMounted(() => {
  const rootElement = document.documentElement;

  // Create an object to animate
  const animTarget = { angle: 90 };

  // Animate the gradient angle with loop and alternate
  angAnim = animate(animTarget, {
    angle: 270,
    duration: 3500,
    easing: 'linear',
    loop: true,
    alternate: true,
    onUpdate: () => {

      rootElement.style.setProperty('--grd-angle', `${animTarget.angle}deg`);
    }
  });
});

onUnmounted(() => {
  angAnim.cancel();
});

</script>
<style scoped lang="scss">

:root {
    --grd-angle: 0deg;
}
#iv-container {
    background-image: linear-gradient(var(--grd-angle), $yellow-1, $red-1);
}
</style>
