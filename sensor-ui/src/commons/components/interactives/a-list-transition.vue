<template>
  <transition-group name="list-complete"
                    :tag="tag" class="relative-position">
    <slot></slot>
  </transition-group>
</template>

<script>
    export default {
        name: "a-list-transition",
        props: {
          tag: {
            type: String,
            default: 'div'
          }
        }
    }
</script>

<style scoped lang="scss">

:deep() {

  .list-complete-move {
    transition: transform 0.6s;
  }
  .list-complete-enter, .list-complete-leave-to
    /* .list-complete-leave-active below version 2.1.8 */ {
    opacity: 0;
    transform: translateY(30px);
  }
  .list-complete-leave-active {

     transition: all 0.5s;
     position: absolute;
     display: block;
  }
}

</style>
