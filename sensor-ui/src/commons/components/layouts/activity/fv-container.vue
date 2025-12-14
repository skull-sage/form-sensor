<template>
  <div class="fullscreen flex flex-center overflow-auto">
    <div class="q-mb-xs-none q-mb-md-lg container q-pa-sm">
      <slot></slot>
    </div>
  </div>
</template>

<script>
    export default {
        name: "fv-container"
    }
</script>

<style scoped lang="scss">

  $container-width: 500px;

  .container{
    width: $container-width;

   @media  (max-width: $container-width){
      width: 100%;
   }
 }
</style>
