<template>
  <a-slide-transition appear
                      v-on="$listeners"
                      v-bind="$attrs"
                      @after-enter="triggerNext"

  >
    <div :key="index">
      <slot :current="current" ></slot>
    </div>
  </a-slide-transition>
</template>

<script>

  let timeOutRef = undefined;

    export default {
        name: "a-grseq-transition",
        props: {
          dataList: Array,
          interval : {
            type: Number,
            default: 2 // in second
          }
        },
        data(){
          return {

            index : 0
          }
        },
        methods:{
          triggerNext(){
            timeOutRef = setTimeout(()=> {
              this.index = (++this.index) % this.dataList.length
            }, this.interval * 1000)
          }
        },
        computed:{
          current(){
            return this.dataList[this.index]
          }
        },
        beforeDestroy() {
          clearTimeout(timeOutRef);
        }
    }
</script>

<style scoped>

</style>
