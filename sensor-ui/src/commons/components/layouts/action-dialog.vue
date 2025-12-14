<template>
  <q-dialog
    transition-show="slide-left"
    transition-hide="slide-left"
    v-bind="$attrs">
    <q-card  :style="widthHint"   >
      <q-card-section class="q-pa-xs-sm flex justify-between">
          <slot name="header">
            <div class="text-bold text-blue-grey-10">{{title}}</div>
            <div class="text-caption text-grey-7" v-if="subtitle">{{subtitle}}</div>
          </slot>
        <q-spinner v-if="loading" />
      </q-card-section>

      <q-separator v-if="separator" />

      <q-card-section :style="heightHint" class="scroll-y  overflow-hidden-x q-py-xs" :class="[contentClz]">
        <slot></slot>
      </q-card-section>

      <q-separator v-if="separator" />

      <q-card-actions align="between" class="q-py-md q-px-md"  >
          <div class="q-gutter-xs">
            <slot name="ctxAction" ></slot>
          </div>
          <div class="q-gutter-xs">
            <slot name="action"></slot>
          </div>
      </q-card-actions>
    </q-card>

  </q-dialog>
</template>

<script>

    export default {
        name: "action-dialog",
        props: {
          title : String,
          subtitle: String,
          medium: Boolean,
          large: Boolean,
          small: Boolean,
          separator: Boolean,
          separatorShadow: Boolean,
          loading: false,
          contentClz: ''
        },
        computed:{
          widthHint(){

            if(this.large)
              return {minWidth: '80vw'};
            else if(this.medium)
              return {minWidth: '50vw'}
            else if(this.small)
              return {width: '320px'}
            else if (this.$q.screen.gt.sm)
              return { minWidth:'380px',  maxWidth: '50vw'};
            else
                return {width: '100%'}
          },
          heightHint(){
             if(this.large)
              return {maxHeight: '70vh'};
            else if(this.medium)
              return {maxHeight: '60vh', height: '60vh'}
            else
              return {maxHeight: '50vh'};
          },

        }
    }
</script>

<style scoped lang="scss">
</style>
