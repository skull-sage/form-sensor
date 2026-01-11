<template>
  <div ref="txtContainer">
     <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { animate } from 'animejs';

// Props
const props = defineProps<{
  audioFile?: string; // Optional audio file name to play during animation
}>();

// Refs
const txtContainer = ref<HTMLElement | null>(null);
let currentAnimation: any = null;
let audioInstance: HTMLAudioElement | null = null;

// Initialize audio if audioFile is provided
if (props.audioFile) {
  audioInstance = new Audio(props.audioFile);
  audioInstance.volume = 0.3; // Set volume to 30% (range: 0.0 to 1.0)
}

// Animate text character by character
const animateText = () => {
  if (!txtContainer.value) return;

  // Cancel any existing animation
  if (currentAnimation) {
    currentAnimation.cancel();
    currentAnimation = null;
  }

  // Get source text and reset container
  let srcTxt = txtContainer.value.textContent || '';
  txtContainer.value.textContent = '';
  let resultTxt = ''

  // Create an object to animate
  const animObj = { index: 0 };

  // Animate the index from 0 to text length
  currentAnimation = animate(animObj, {
    index: srcTxt.length-1,
    duration: srcTxt.length * 100, // 50ms per character
    easing: 'linear',
    onUpdate: () => {
      // Update textContent with characters up to current index
      const currentIndex = Math.floor(animObj.index);
      for (let i = resultTxt.length; i <= currentIndex; i++) {
        resultTxt += srcTxt[i];

        // Play audio beep for each new character
        if (audioInstance) {
          audioInstance.currentTime = 0; // Reset to start
          audioInstance.play().catch(err => {
            console.warn('Audio play failed:', err);
          });
        }
      }
      txtContainer.value.textContent = resultTxt;
    },
  });
};

// On mount, get innerHTML text and start animation
onMounted(() => {
  if (txtContainer.value) {
    animateText();
  }
});

// Cleanup on unmount
onBeforeUnmount(() => {
  if (currentAnimation) {
    currentAnimation.cancel();
    currentAnimation = null;
  }

  // Cleanup audio
  if (audioInstance) {
    audioInstance.pause();
    audioInstance = null;
  }
});
</script>

<style scoped>

</style>
