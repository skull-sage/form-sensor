<template>
  <div class="expandable"  :style="[]">
    <slot></slot>
    <a-btn tertiary :label="label"/>
  </div>
</template>

<script>
    export default {
        name: "an-expandable",
        props: ['height'],
        data(){
          return {
            expanded : false
          }
        },
        computed: {
          label(){
            if(this.expanded)
              return 'VIEW LESS'
            else return 'VIEW MORE'
          }
        }
    }
</script>

<style scoped>

</style>
