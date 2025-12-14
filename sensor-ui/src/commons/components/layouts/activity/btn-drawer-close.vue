<template>
  <a-btn v-bind="$attrs"
         size="sm"
         action primary round
         icon="r_close"
         @click="hideDrawer"

  />
</template>

<script setup>
import {inject} from "vue";
const {hideDrawer} = inject("drawer_state")
</script>

<style scoped>

</style>
