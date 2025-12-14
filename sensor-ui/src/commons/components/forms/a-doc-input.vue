<template>
  <a-btn neutral secondary size="lg" :label="`ADD ${label}`"
         class="full-width"
         v-if="!initiated"
         @click="initiated = true"
  />
  <div v-else class="editor-field bg-grey-2 q-pa-sm">
    <div class="control-bar flex justify-between items-start">
      <div class="text-caption text-uppercase">{{label}}</div>
      <div>
        <a-btn size="sm" dense neutral tertiary
               icon="r_clear_all"
               @click="initiated = false, $refs.editor.clearDoc()"
        />
      </div>
    </div>

    <editor-doc-basic ref="editor"
                      class="q-pa-xs"
                      :model-value="value"
                      @input="$emit('input', $event)"
                      :blob-ref="blobRef"
    />
  </div>
</template>

<script>
export default {
  name: "a-doc-input",
  props: ['value', 'blobRef', 'label'],
  watch:{
    'value': {
      handler(){
        if(this.value)
          this.initiated = true;
      },
      immediate: true
    }
  },
  data(){
    return {
      initiated: false
    }
  }
}
</script>

<style scoped lang="scss">
.control-bar .text-caption{
  transition: color 300ms ease;
}
  .editor-field:focus-within{
    .control-bar .text-caption{
      color: $primary;
    }
  }
  .control-bar{
    height: $space-base;
  }
</style>
