<template>
<div class="fullscreen flex flex-center" id="iv-container">

  <div style="width: 1080px;" class="q-pa-xl">
    <div class="text-bold text-h5 q-mt-md">
      Rashed's Interview
    </div>
    <div class="row full-width">
      <div class="col-md-6">
        <div ref="qBox"></div>
      </div>
      <div class="col-md-6">
        <MicStream ref="micStream" class="rounded-borders shadow-8"
            @recorded-chunk="handleRecordedChunk" />

        </div>
    </div>
  </div>

</div>
</template>
<script setup lang="ts">
import MicStream from './mic-stream.vue';
import { reactive, ref, onMounted, onUnmounted } from 'vue';
import { animate } from 'animejs';
import { analyzeAudio } from './cv-api';

const micStream = ref<InstanceType<typeof MicStream> | null>(null)

const qList = reactive([
  'Hi There! How have been your day?',
  "introduce yourself",
  "tell me your job experience relevant to AI Chocolate"])

let qIdx = ref(0)

// Animation instance for cleanup
let angAnim: any = null;

const handleRecordedChunk = async (blob: Blob, duration: number) => {
  let {text:answer, score} = await analyzeAudio(blob, qList[qIdx.value]);
    if (score > 0.6 && qIdx.value < qList.length - 1) {
      if (qIdx.value < qList.length - 1) {
            qIdx.value++
      }
    }
}


onMounted(() => {
  const rootElement = document.documentElement;

  // Create an object to animate
  const animTarget = { angle: 90 };

  // Animate the gradient angle with loop and alternate
  angAnim = animate(animTarget, {
    angle: 270,
    duration: 2000,
    easing: 'linear',
    loop: true,
    alternate: true,
    onUpdate: () => {
      console.log(animTarget.angle)
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
