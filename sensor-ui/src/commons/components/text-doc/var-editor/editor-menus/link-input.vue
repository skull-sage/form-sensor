<template>
  <a-btn icon="r_link" @click="inputVisible = true">
    <action-dialog title="link-input" v-model="inputVisible">
      <q-input label="URL" v-model="hrefUrl" type="url" />
      <template #actions>
        <a-btn action primary label="SAVE" @click="saveHref" />
      </template>
    </action-dialog>
  </a-btn>
</template>

<script>

export default {
  name: "link-input",
  props: ["editorView"],
  data(){
    return {
      hrefUrl: undefined,
      inputVisible: false
    }
  },
  methods:{
    showUrlInput(){
      this.hrefUrl = undefined;
      this.inputVisible = true;
    },
    saveHref(){
      let {state, dispatch} = this.editorView;
      let {from, to} = state.selection;
      let  anchorTxt = state.doc.textBetween(from, to);
      let nodeJson = {
        type: 'ext_link',
        attrs: {href: this.hrefUrl, anchorTxt: anchorTxt},
      };
      let anchorNode = state.schema.nodeFromJSON(nodeJson);
      let _tr = state.tr.replaceSelectionWith(anchorNode);
      dispatch(_tr);
      this.inputVisible = false;
    }
  }

}
</script>

<style scoped>

</style>
