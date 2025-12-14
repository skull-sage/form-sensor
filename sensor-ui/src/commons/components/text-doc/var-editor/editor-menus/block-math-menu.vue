<template>
  <div class="bg-blue-grey-9 text-white shadow-4">
    <a-btn  label="Delete" tertiary dark @click="removeNode()" />
    <block-math-input  label="Edit math" tertiary dark
                        :editor-view="editorView" />

  </div>
</template>

<script>
import BlockMathInput from "./block-math-input";

export default {
  name: "math-menu",
  components: {BlockMathInput},
  props: ['editorView'],
  methods:{
    removeNode(){

      let {state, dispatch} = this.editorView;
      /*let nodeType = state.schema.nodes[this.nodeTypeName];
      let {node, pos} = findSelectedNodeOfType(nodeType)(state.selection);*/
      dispatch(state.tr.deleteSelection());

    }
  }
}
</script>

<style scoped>

</style>
