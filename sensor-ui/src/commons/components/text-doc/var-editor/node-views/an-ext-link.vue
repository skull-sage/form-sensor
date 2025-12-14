<template>
  <span>
    <a :href="linkData.href" @click.prevent="">{{linkData.anchorTxt}}</a>
   <q-popup-proxy ref="popUp" @keyup.enter="$refs.popUp.hide()">
     <div class="q-pa-xs q-gutter-xs" style="width: 400px">
      <an-input v-model="linkData.href" @input="$emit('input', linkData)"
                type="url" label="Href URL"/>
      <an-input v-model="linkData.anchorTxt" @input="$emit('input', linkData)"
                type="text" label="Anchor Text"/>
     </div>
    </q-popup-proxy>
  </span>
</template>

<script>
export default {
 name: "an-ext-link",
 data(){
   return {
     linkData: {
       href: undefined,
       anchorTxt: undefined
     }
   }
 },
  methods:{
    initData(data$){
      this.linkData = data$;
    }

  }
}
</script>

<style scoped>

</style>
