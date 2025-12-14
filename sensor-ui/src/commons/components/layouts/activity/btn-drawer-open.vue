<template>
  <q-btn v-bind="$attrs"
         flat dense icon="r_menu"
         @click="showDrawer"
  />
</template>

<script setup>
import {inject} from "vue";
const {showDrawer} = inject("drawer_state")
</script>

<style scoped>

</style>
