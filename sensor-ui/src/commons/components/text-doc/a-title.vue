<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "a-title",
  props: {
    st: Boolean,
    sst: Boolean,
    weightBolder: Boolean,
    weightBold: Boolean,
    weightMedium: Boolean,
    weightThin: Boolean,
    weightLight: Boolean,
  },
  computed: {
    weight() {
      if (this.weightBolder) return 'text-weight-bolder'
      if (this.weightBold) return 'text-weight-bold'
      if (this.weightMedium) return 'text-weight-medium'
      if (this.weightThin) return 'text-weight-thin'
      if (this.weightLight) return 'text-weight-light'
      return 'text-weight-regular'
    },
  },
})
</script>

<template>
  <h2 v-if="st" class="title-h2" :class="[weight]" ><slot></slot></h2>
  <h3 v-else-if="sst" class="title-h3"  :class="[weight]" ><slot></slot></h3>
  <h1 v-else class="title-h1" :class="[weight]" ><slot></slot></h1>
</template>

<style scoped>

</style>
