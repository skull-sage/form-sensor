<template>
  <q-btn
    :dense="dense"
    :label="label" :icon="icon"
    :size="size"
    :fab="fab"
    :fab-mini="fabMini"
    :class="[gradientClz]"
    class="shadow-1 text-white"
    :loading="loading"
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
    name: "gradient-btn",
    extends: ARouteBase,
    props:{
      gtagLabel : String,
      gtagCategory: String,
      loading: Boolean,
      label: String,
      icon : String,
      size: String,
      dense: Boolean,
      fab : Boolean,
      fabMini: Boolean,
      // style
      //primary: Boolean,
      /**
       * if neither secondary or tertiary it is assumed to be primary
       * */
      primary :  Boolean,
      secondary: Boolean,
      tertiary: Boolean,

      // to route
      to : String | Object,
      routeName: String,
      routeParams: Object,
      routeQuery: Object,

    },

    computed:{

      gradientClz(){
        if(this.tertiary)
          return 'bg-gradient-orange'
        else if(this.secondary)
          return 'bg-gradient-teal'
        else
          return 'bg-gradient-blue'
      },


    }

  }

</script>

