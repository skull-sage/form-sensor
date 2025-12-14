<template>
  <q-tabs
          class="text-blue-grey-4  "
          :active-color="activeColor"
          active-bg-color="transparent"
          :indicator-color="activeColor"
          :align="align"
          v-bind="$attrs" >

          <template v-for="(_, slot) in $slots" v-slot:[slot]="scope">
            <slot :name="slot" v-bind="scope || {}" />
          </template>

  </q-tabs>
</template>

<script>
    export default {
        name: "a-tabs",
        props: {
          accent: Boolean,
          align: {
            type: String,
            default: 'left'
          }
        },
        computed:{
          activeColor(){
            if(this.accent)
              return 'teal-9'
            else return 'blue-grey-10'
          }
        }

    }
</script>

<style scoped lang="scss">

</style>
