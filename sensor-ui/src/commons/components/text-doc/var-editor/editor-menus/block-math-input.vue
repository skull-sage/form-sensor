<template>
  <a-btn tertiary dense @click.stop="openEditor()" v-bind="$attrs">
    <action-dialog :model-value="editorVisible"
                     separator medium
                   title="Math Editor">
      <template #default>
        <div class="row q-col-gutter-sm full-height"  >
          <div class="col-xs-12 col-md-6">
            <q-input  class="math-editor full-width " wrap
                      type="textarea" debounce="300"
                      v-model="mathLatex" @input="updateMath"
                      placeholder="Start typing \sqrt(x) + b"/>
          </div>
          <div class="col-xs-12 col-md-6">
            <div v-html="mathHtml" class="full-height overflow-auto text-caption"
                 :class="[hasError ? 'text-red': '']" />

          </div>
        </div>
      </template>
      <template #actions>
        <a-btn neutral tertiary label="cancel" @click="editorVisible = false"/>
        <a-btn action tertiary label="save" @click="saveMath()" />
      </template>
    </action-dialog>
  </a-btn>

</template>

<script>
import utlDebounce from 'lodash/debounce'
import {findSelectedNodeOfType} from "../utils";
import {blockMathHtml} from "src/commons/utils/math-util";
export default {
  name: "block-math-input",
  props: ['editorView'],
  data(){
    return {
      mathLatex : '',
      editorVisible: false,
      mathHtml : undefined,
      hasError: true
    }
  },


  /*computed:{
    mathHtml(){
      return blockMathHtml(this.mathLatex);
    }
  },*/
  methods:{

    /*updateMath: utlDebounce(function ($event) {
      this.mathLatex = $event
    }, 300),*/

    updateMath(){
      try{
        this.hasError = false;
        this.mathHtml = blockMathHtml(this.mathLatex)  ;
        console.log(this.mathHtml)
      }catch (err){
        this.hasError = true;
        this.mathHtml = err;
      }
    },
    openEditor(){
      this.editorVisible = true;
      let {state} = this.editorView;
      let selection = findSelectedNodeOfType(state.schema.nodes.block_math)(state.selection);
      if(selection)
      {
        this.mathLatex = selection.node.attrs.latex;
      }

    },

    saveMath(){

      this.editorVisible = false;
      let {state, dispatch} = this.editorView;
      let selection = findSelectedNodeOfType(state.schema.nodes.block_math)(state.selection);

      if(!selection)
      {
        if(this.mathLatex.trim().length == 0)
          return;
        let node = state.schema.node('block_math');
        node.attrs = {latex : this.mathLatex};
        dispatch(state.tr.replaceSelectionWith(node));
      }
      else{
        let copy = selection.node.copy();
        copy.attrs = {latex : this.mathLatex};
        dispatch(state.tr.replaceSelectionWith(copy));
      }


    }
  }
}
</script>

<style scoped lang="scss">
.math-editor{

  border: none;
  resize: none;
  background: $grey-1;
  &:focus{
    outline: none;
  }
}
</style>
