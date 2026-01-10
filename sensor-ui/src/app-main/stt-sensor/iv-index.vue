<template>
<div class="fullscreen flex flex-center" id="iv-container">

  <div style="width: 1080px;" class="q-pa-xl">
    <div class="text-bold text-h5 q-mt-md q-mb-lg">
      Rashed's Interview
    </div>
    <div class="row full-width">
      <div class="col-md-6 q-mt-lg">
        <SmartTxt ref="qBox">{{ currentQ.query }}</SmartTxt>
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

const micStream = ref<InstanceType<typeof MicStream> | null>(null)
const qBox = ref<HTMLElement | null>(null)

const currentQ = computed(() => cvAPI.currentQ())
watch(currentQ, () => {
  if (qBox.value) {
    animate(qBox.value, {
      opacity: [0, 1],
      duration: 500,
      easing: 'ease-in-out',
    })
    qBox.value.innerHTML = currentQ.value.query
  }
})

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
    duration: 2000,
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
