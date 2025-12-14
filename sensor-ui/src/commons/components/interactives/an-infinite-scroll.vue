<template>
  <q-infinite-scroll ref="infiniteScroll"
                     v-on="$listeners"
                     v-bind="$attrs" :offset="500" :dbounce="500">
       <slot> </slot>
       <a-warning v-if="noMoreData">No more data to show</a-warning>
    <template #loading>
      <a-spinner />
    </template>
  </q-infinite-scroll>
</template>

<script>
export default {
  name: "an-infinite-scroll",
  props: ['noMoreData'],
  methods:{
    reset(){
      this.$refs.infiniteScroll.reset();
    },
   /* stop(){
      this.$refs.infiniteScroll.stop();
    }*/
  }
}
</script>

<style scoped>

</style>
