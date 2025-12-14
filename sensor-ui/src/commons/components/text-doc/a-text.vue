<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "a-text",
  props: {
    bold: Boolean,
    caption: Boolean,
  },
})
</script>
<template>
  <p :class="{'text-bold': bold, 'a-caption': caption}"><slot></slot></p>
</template>

<style scoped>
.a-caption {
  opacity: 0.5;
  font-size: 14px;
}
</style>
