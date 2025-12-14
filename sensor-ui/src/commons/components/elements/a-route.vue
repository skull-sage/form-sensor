<template>
  <router-link :to="calcRoute"
               v-on="$listeners"
               @click.native="triggerGtag('route-link')">
    <slot></slot>
  </router-link>
</template>

<script>
  import RouteBase from './a-route-base.vue'
    export default {
        name: "a-route",
        extends: RouteBase

    }
</script>

<style scoped>
  a {
    text-decoration: none;
    color: inherit;
    transition: opacity linear 300ms;
  }
  a:hover{
    opacity: 0.7;
  }
</style>
