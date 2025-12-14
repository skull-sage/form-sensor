<template>
  <q-page>
    <slot></slot>

    <q-page-sticky expand position="top" ref="stickyTop" v-if="$slots.stickyTop"  >
        <div class="full-width">
          <slot name="stickyTop"></slot>
        </div>
    </q-page-sticky>
    <q-page-sticky expand position="bottom" ref="stickyBottom"  >
      <a-section class="full-width"><slot name="stickyBottom"></slot></a-section>
    </q-page-sticky>

    <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
      <a-btn   fab icon="r_keyboard_arrow_up" action primary class="shadow-1" />
      <!--<gradient-btn  fab-mini icon="keyboard_arrow_up" size="sm" primary class="xs" />-->
    </q-page-scroller>
  </q-page>
</template>

<script>
  import {calcElmBox} from 'src/commons/utils/dom-util.js'

    export default {
        name: "a-page",

        mounted() {0

          this.$nextTick(this.domUpdateHook);
        },
        updated() {
          this.$nextTick(this.domUpdateHook);
        },
        methods:{
          domUpdateHook(){
            if(this.$el)
            {
              if(this.$refs.stickyTop){
                  let stickyTopBox = calcElmBox(this.$refs.stickyTop.$el);
                  this.$el.style.paddingTop = (stickyTopBox.offsetHeight)+ "px" ;

              }
              else {
                  this.$el.style.marginTop = "-1px";
              }

                if(this.$refs.stickyBottom){
                    let stickyBottomBox = calcElmBox(this.$refs.stickyBottom.$el);
                    this.$el.style.paddingBottom = (stickyBottomBox.offsetHeight - 1)+ "px" ;
                }

            }

          }
        }
    }
</script>

<style scoped>
 :deep(a.anchor) {
   display: block;
   position: relative;
  visibility: hidden;
 }
 /*.sticky-bar{
   margin-top: -1px;
 }*/

</style>
