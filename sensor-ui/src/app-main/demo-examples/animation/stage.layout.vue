<script setup lang="ts">

</script>

<template>
  <div>
    <div class="row q-gutter-md">
      <q-responsive :ratio="9/16" class="col border">
          <div class="bg-blue-1  relative-position">
            <div class="absolute-top">Input Canvas</div>
            <slot name="input"></slot>
          </div>
      </q-responsive>
      <q-responsive :ratio="9/16" class="col border">
        <div class="bg-blue-1  ">
          <div class="absolute-top">Output Canvas</div>
          <slot name="output"></slot>
        </div>
      </q-responsive>
    </div>
  </div>
</template>

<style scoped>
  .border {
    border: 1px lightgrey dashed;
  }
</style>
