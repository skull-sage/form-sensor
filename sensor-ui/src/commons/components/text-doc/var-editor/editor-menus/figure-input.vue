<template>
  <a-btn dense tertiary v-bind="$attrs"
          @click="$refs.fileInput.click()"
          :loading="reqTrying">
    <input ref="fileInput" type="file" class="file-input"
           @change="onFileSelected($event.target.files)">
  </a-btn>
</template>

<script>

export default {
  name: "figure-input",
  props: ['editorView'],
  methods:{
    async onFileSelected(files$){


      let file = files$[0];
      this.$refs.fileInput.value = "";
      //alert(`size ${file.size} type ${file.type}`)

      const lastDot = file.name.lastIndexOf('.');
      const ext = file.name.substring(lastDot + 1);
      let reqData = {
              blob_ref: this.editorView.blobRef,
              meta: {
                extension : ext,
                content_type: file.type}
      }
      this.initReq();
      try{
        let {data, status} = await this.$blobApi.command('GenerateURL', reqData);
        await this.$blobUploader(data.cdn_url, file, data.meta);
        this.reqSuccess();
        this.insertInEditor( data.cdn_url, data.meta.key);

      }catch (error$)
      {

        this.reqFailed('Figure Upload Failed')
      }

    },
    insertInEditor(cdn$, key$){
      let {state, dispatch} = this.editorView;

      let figureNode = state.schema.node('figure');
      figureNode.attrs = { blob: {cdn: cdn$, key: key$}};

      let tr = state.tr.replaceSelectionWith(figureNode);
      dispatch(tr);
    },
  }
}
</script>

<style scoped>
.file-input{
  visibility: hidden;
  width: 0;
  height: 0;
}
</style>
