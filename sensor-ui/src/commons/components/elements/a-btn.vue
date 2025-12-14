<template>
  <q-btn
    :color="colorCalc"
    :text-color="textColor"
    :outline="outline"
    :flat="flatCalc"
    unelevated
    :class="[shadow]"
    v-bind="$attrs"
    :to="calcRoute"
  >
    <slot></slot>
    <slot name="badge"></slot>
  </q-btn>
</template>

<script>
import ARouteBase from './a-route-base.vue'

    export default {
        name: "a-btn",
        extends: ARouteBase,
        props:{

          color: String,
          action: Boolean,
          accent: Boolean,
          warning: Boolean,
          danger: Boolean,
          neutral: Boolean,
          // style
          //primary: Boolean,
          /**
           * if neither secondary or tertiary it is assumed to be primary
           * */
          primary :  Boolean, // filled
          secondary: Boolean, // outlined
          tertiary: Boolean, // flat



        },
        computed:{


          textColor(){
            if(this.neutral)
              return 'grey-8'
          },
          colorCalc(){
            if(this.color)
                return this.color;

            if(this.neutral)
              return "white"
            if(this.action)
              return "indigo-13"
            else if(this.accent)
              return "cyan-8"
            else if(this.warning)
                return "amber-13"
            else if(this.danger)
                return "red-7"

          },

          outline(){
            if(this.secondary)
              return this.secondary;
          },

          flatCalc(){
             return this.tertiary;
            },

          shadow(){
            if(this.primary)
              return 'shadow-2'
            else
              return 'shadow-0'
          }
        }

    }

</script>

<style scoped lang="scss">

  :deep(.q-icon) {
    opacity: 0.8;
  }
 /* .accent-indigo{
    color: white;
    background-image: $grd-indigo-lr;
  }
  .accent-teal{
    color: white;
    background-image: $grd-teal-lr
  }

  .accent-orange{
    color: white;
    background-image: $grd-orange-lr
  }*/
</style>
