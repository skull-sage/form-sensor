<template>
  <a class="row justify-center q-col-gutter-sm">
    <div class="col-xs-12 col-sm-12 col-md-6 flex justify-center" :class="[order.snippet]">
      <slot name="snippet"></slot>
    </div>
    <div class="col-xs-12 col-sm-11 col-md-6 flex flex-center " :class="[order.dialogue]">
      <div :class="[textAlign]" class="q-ml-xs-none q-ml-md-md">
        <h2 class="title-h2 text-weight-bolder q-mb-sm" :class="[titleBaseColor]">
          <slot name="title"></slot>
        </h2>
        <div class="title-h3 text-weight-light q-mb-sm q-px-xs-sm q-px-md-none" :class="[titleBaseColor]" >
          <slot name="subtitle"></slot>
        </div>
        <slot name="ctaBtn" v-if="!smallScreen"></slot>
      </div>
    </div>
    <div class="col-xs-12 order-last text-center q-my-sm" v-if="$slots.ctaBtn && smallScreen">
      <slot name="ctaBtn"></slot>
    </div>
  </a>
</template>

<script>
    export default {
        name: "a-hl-section",
        props: {
          baseColor: { type: String, default : 'blue-grey-9'},
          dialogueFirst : {type : Boolean, default: false},
          dark:{
            type: Boolean,
            default: false
          }
        },
      data(){
          return {
            flexOrder : {
              dialogue : 'order-first',
              snippet : 'order-last'
            },
          }
      },
      computed: {

          smallScreen(){
            return this.$q.screen.lt.md || false;
          },
          order()
          {
            if(this.smallScreen || this.dialogueFirst)
            {
              this.flexOrder.dialogue = 'order-first';
              this.flexOrder.snippet = 'order-last';
            }
            else
            {
              this.flexOrder.snippet = 'order-first'
              this.flexOrder.dialogue = 'order-last'
            }

            return this.flexOrder;
          },

           textAlign(){
            if(this.smallScreen)
              return 'text-center'
            return 'text-left'
           },

          titleBaseColor(){
            if(this.dark)
              return  'text-grey-1'
            return 'text-'+this.baseColor
          }
      }

    }
</script>

<style scoped>

</style>
