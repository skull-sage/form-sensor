<template>
<div style="width: 500px;">
  <div class="text-h5 text-bold">
    Thank you so much for your time.
  </div>
  <SmartTxt :audio-file="roboBeep">We generally take 1-2 weeks to process your application. We will be in touch with you soon.</SmartTxt>
</div>
</template>

<script setup lang="ts">
import SmartTxt from './smart-txt.vue';
import roboBeep from './robo-beep-30.wav';

</script>

