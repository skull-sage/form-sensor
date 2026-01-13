<template>
<div class="fullscreen flex flex-center  iv-container" >
  <IvStreamInit @stream-ready="startInterview" v-if="ivState === 'NOT_STARTED'"/>
  <div style="width: 1080px;" class="q-pa-xl" v-else-if="ivState === 'STARTED'">
    <div class="text-bold text-h5 q-mt-md q-mb-lg">
      <span class="text-grey-5">Interview |</span> MLOps Software Engineer
      <div class="text-body1"><span class="text-grey-5">Jan 14, 2026</span> Mr. Skull</div>
    </div>
    <div class="row full-width">
      <div class="col-md-6 q-mt-lg">
        <SmartTxt class="text-purple-10" :key="currentQ.id" :audio-file="roboBeep">{{ currentQ.query }}</SmartTxt>
        <q-spinner v-if="evalProgress" />
        <div v-else-if="currentQ.eval!.ans" class="q-px-md q-my-md" style="border-left: 1px solid #ccc;">
          <div class="text-body1  ">
            {{ currentQ.eval.ans }}
          </div>
          <div class="text-caption text-teal-10">
            {{ currentQ.eval.score }}
          </div>
        </div>
      </div>
      <div class="col-md-6 justify-center">
        <IvRecorder  :mic-stream="micStream" class="rounded-borders shadow-8"
            @recorded-chunk="handleRecordedChunk" />

        </div>
    </div>
  </div>
  <IvComplete v-else-if="ivState === 'COMPLETED'"/>
</div>
</template>
<script setup lang="ts">
import MicStream from './mic-stream.vue';
import { reactive, ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { animate } from 'animejs';
import cvAPI from './cv-api';
import SmartTxt from './smart-txt.vue';
import roboBeep from './robo-beep-30.wav';
import IvStreamInit from './iv-stream-init.vue';
import IvRecorder from './iv-recorder.vue';
import IvComplete from './iv-complete.vue';


// Interview state enum
type IvState = 'NOT_STARTED' | 'STARTED' | 'COMPLETED'

const ivState = ref<IvState>('NOT_STARTED')
const currentQ = computed(() => cvAPI.currentQ())
const micStream = ref<MediaStream | null>(null)
const evalProgress = ref(false)

const startInterview = (camStream: MediaStream) => {
  micStream.value = camStream
  ivState.value = 'STARTED'
}

const handleRecordedChunk = async (blob: Blob, duration: number) => {
  evalProgress.value = true
  await cvAPI.analyzeAudio(blob);
  if (cvAPI.isLastQ()) {
    setTimeout(() => ivState.value = 'COMPLETED', 3000)
  }
  evalProgress.value = false
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
.iv-container {
    background-image: linear-gradient(var(--grd-angle), $yellow-1, $red-1);
}
</style>
