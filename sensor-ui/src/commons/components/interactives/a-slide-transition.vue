<template>
  <transition
    :enter-class="computedEnter"
    :enter-active-class="computedActive"
    :leave-active-class="computedActive"
    :leave-to-class="computedLeaveTo"
    v-on="$listeners"
    :mode="mode"
    v-bind="$attrs"
  >
    <slot></slot>
  </transition>
</template>

<script>
  export default {
    name: "a-slide-transition",
    props: {
      mode:{
        type: String,
        default:'out-in'
      },
      enter:  {
        type: String,
        default: 'left',
      },
      leave: {
        type: String,
        default: 'right',
      },
      fadeOnly:{
        type: Boolean,
        default: false // or slide-fade
      },
      slower: Boolean,
      faster: Boolean
    },

    computed:
      {

        computedEnter()
        {
          if(this.fadeOnly)
            return 'fade-only';
          return  `slide-${this.enter}`

        },

        computedActive()
        {
          return 'slide-fade-active'


        },


        computedLeaveTo()
        {
          if(this.fadeOnly)
            return 'fade-only';
          return   `slide-${this.leave}`

        }

      }
  }
</script>

<style scoped>

  .fade-only {
    opacity: 0;
  }


  .slide-left
  {

     transform: translate(-100%, 0);
     opacity: 0;
  }

  .slide-right
  {

     transform: translate(100%, 0);
     opacity: 0;
  }
  .slide-top
  {
    transform: translate(0, -100%);
    opacity: 0;
  }
  .slide-bottom
  {
    transform: translate(0, 100%);
    opacity: 0;
  }


  .slide-fade-active
  {
    transition-property: transform, opacity;
    transition-timing-function: ease;
    transition-duration: 0.4s;
  }


</style>
