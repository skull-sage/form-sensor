<template>
  <q-item clickable :to="calcRoute"
          @click="triggerGtag('nav-item')">
    <slot></slot>
  </q-item>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ARouteBase from "./a-route-base.vue";

export default defineComponent({
  name: "a-nav-item",
  extends: ARouteBase,
  computed:{}
})
</script>
