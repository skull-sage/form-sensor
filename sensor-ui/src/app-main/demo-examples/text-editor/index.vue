<script >
import {defineAsyncComponent, isReactive, isShallow, markRaw, ref, shallowReactive, toRaw} from "vue";
import {sleepFunc} from "src/commons/utils/async-dummy.js";

let BasicEditor = defineAsyncComponent(()=> import("src/commons/components/editor/index.vue"))




export default {
  components: {BasicEditor},
  data(){
    return {

      loading: false,
      content: {
        type: "doc",
        content: []
      }
    }
  },


  mounted() {

  }


}
</script>

<template>
  <div class="full-width full-height bg-grey-3 q-pa-xl">

    <div class="row q-col-gutter-sm bg-white">
      <div class="col-6">
        <BasicEditor v-model="content"/>
      </div>
      <div class="col-6">
        <h3 class="text-h6 q-mb-none">Content</h3>
        <pre><code>{{ content }}</code></pre>
      </div>
    </div>
  </div>
</template>

<style scoped  >
</style>
