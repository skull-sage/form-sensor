<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "a-caption",

})
</script>

<template>
  <div class="a-caption"><slot></slot></div>
</template>

<style scoped>
  .a-caption {
    font-size: 1rem;
    opacity: 0.5;
  }
</style>
