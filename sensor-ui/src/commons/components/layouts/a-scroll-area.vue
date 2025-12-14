<template>
  <q-scroll-area
    ref="scrollBox"
    :thumb-style="thumbStyle"

  >
    <slot></slot>
  </q-scroll-area>
</template>

<script>
  import {calcElmBox} from 'src/commons/utils/dom-util.js'

    export default {
        name: "a-scroll-area",
        props: {

          windowHeight: Boolean
        },
        data(){
            return {
              thumbStyle: {
                right: '0px',
                borderRadius: '5px',
                backgroundColor: '#027be3',
                width: '5px',
                opacity: 0.75
              }/*,

              barStyle: {
                right: '2px',
                borderRadius: '9px',
                backgroundColor: '#027be3',
                width: '9px',
                opacity: 0.2
              }*/
            }
          },
        updated()
        {
          this.$nextTick(this.domUpdateHook);
        },
        mounted() {
            this.$nextTick(this.domUpdateHook);
        },
        methods:{
          domUpdateHook(){
            if(this.windowHeight)
            {
              let elm = this.$el;
              let box = calcElmBox(elm);
              elm.style.height = (window.innerHeight - box.top - box.marginTop - box.marginBottom - 1) + "px";
            }
          }
        }
    }
</script>

<style scoped>

</style>
