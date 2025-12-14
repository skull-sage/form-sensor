<template>
  <div class="flex justify-center" :class="[paddingClz]">
    <svg id="load-spinner" x="0px" y="0px" viewBox="0 0 150 150">
      <linearGradient id="gradient">
        <stop class="main-stop" stop-color="#0096a5" offset="0%" /> <!--lojens-cyan-->
        <stop class="main-stop" stop-color="#53b197" offset="33%" /> <!--lojens-teal-->
        <stop class="main-stop" stop-color="#f9c130" offset="78%" /> <!--lojens-yellow-->
        <stop class="alt-stop"  stop-color="#d35e54" offset="100%" /> <!--lojens-read-->
      </linearGradient>
      <circle id="loading-inner" cx="75" cy="75" r="60" stroke="url(#gradient)"></circle>
    </svg>
    <!--<q-spinner-hourglass color="red-7" size="2em"/>-->
  </div>


</template>

<script>
    export default {
        name: "a-spinner",
        props:{
          paddingClz : {
            type: String,
            default: 'q-pa-lg'
          }
        }
    }
</script>

<style scoped>
.semi-center
{
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate3d(-50%, -50%, 0);
}
</style>
