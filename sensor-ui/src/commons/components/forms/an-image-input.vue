<template>
  <figure
    class="bg-grey-1 flex flex-center overflow-hidden relative-position outline-1 text-grey-3"
    @click="$refs.fileInput.click()"
    :style="calcStyle">
    <div  v-if="!value" class="text-grey-6 text-center text-caption" >
      <div >W(min{{minWidth}}, max{{maxWidth}})px</div>
      <div>W:H = {{aspect.toFixed(3)}}
        <strong class="text-blue-grey-7">:</strong>1.0
      </div>
      <a-btn neutral secondary label="Thumbnail" icon="r_add" />
    </div>
    <img v-else :src="value" class="img-responsive-x" />
    <input ref="fileInput" type="file" class="file-input absolute-top-right"
           @change="onFileSelected($event.target.files)">
    <q-inner-loading :showing="reqTrying">
      <a-spinner />
    </q-inner-loading>
  </figure>
</template>

<script>
import AField from './a-field.vue'
import {calcElmBox} from 'src/commons/utils/dom-util'
export default {
  name: "an-image-input",
  components: {AField},
  props:
    {
      value: undefined,
      label: String,
      blobRef: Array, // :blob-ref="['sports', 'ft-cricket', 'player', 213]"
      minWidth: {
        type: Number,
        default: 600,
      },
      maxWidth: {
        type: Number,
        default: 1200
      },
      aspect: {
        type: [Number], // aspect::string : 'fb',  'square'
        default: 1.912/1 // fb-aspect
      },

      maxSize: Number, // in mb
    },
  data(){
    return {
      calcStyle: undefined
    }
  },
  mounted() {
    this.$nextTick(() => {
      let box = calcElmBox(this.$el);

      let height = box.clientWidth / this.aspect;
      this.calcStyle = { height: height + 'px' }
    });

  },

  computed:{
    calcAspect(){

    },
  },

  methods:{
    async tryDeletePrevious(){
      try{
        this.initReq();
        let pathKey = new URL(this.value).pathname;
        let reqData = {object_key_list: [pathKey]};
        await this.$blobApi.command('DeleteBlob', reqData);
        this.reqSuccess();
      }catch (error$){
        this.reqFailed('Could Not Remove Previous Thumbnail');
        throw error$;
      }
    },
    async onFileSelected(files$){

      try{
        if(this.value)
          await this.tryDeletePrevious();

        let file = files$[0];
        this.$refs.fileInput.value = "";
        //alert(`size ${file.size} type ${file.type}`)
        let sizeInMB = file.size / (1024 * 1024);
        if(sizeInMB > this.maxSize)
        {
          this.reqFailed(`Max Allowed File Size is ${this.maxSize}mb`)
          return ;
        }
        const lastDot = file.name.lastIndexOf('.');
        const ext = file.name.substring(lastDot + 1);
        let reqData = {
          blob_ref: this.blobRef,
          meta: {
            extension : ext,
            content_type: file.type}
        }
        this.initReq();

        let {data, status} = await this.$blobApi.command('GenerateURL', reqData);
        await this.$blobUploader(data.cdn_url, file, data.meta);
        this.reqSuccess();
        let imgSrc = `${data.cdn_url}/${data.meta.key}`;
        this.$emit('input', imgSrc);


      }catch (error$)
      {
        this.reqFailed('Image Upload Failed')
      }

    },
  }
}
</script>

<style scoped>
.file-input{
  display: none;
  width: 0px;
  height: 0px;
}

.input-size-hint
{
  max-width: 600px;
  height: auto;
}
</style>


<style scoped>

</style>
