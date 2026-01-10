<template>
  <div ref="txtContainer">
     <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { animate } from 'animejs';

// Refs
const txtContainer = ref<HTMLElement | null>(null);
let currentAnimation: any = null;

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
    duration: srcTxt.length * 50, // 50ms per character
    easing: 'linear',
    onUpdate: () => {
      // Update textContent with characters up to current index
      const currentIndex = Math.floor(animObj.index);
      for (let i = resultTxt.length; i <= currentIndex; i++) {
        resultTxt += srcTxt[i];
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
});
</script>

<style scoped>

</style>
