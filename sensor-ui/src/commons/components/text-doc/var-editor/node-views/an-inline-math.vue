<template>
  <span  class="inline-math"   latex="">
    <span ref="content"  v-html="mathHtml"></span>
      <q-popup-edit v-model="mathLatex" @save="$emit('input', $event)">
        <template v-slot="scope">
          <q-input autofocus dense
                   v-model="scope.value"
          >
            <template v-slot:after>
              <q-btn flat dense color="negative" icon="r_cancel" @click.stop="scope.cancel" />
              <q-btn flat dense color="positive" icon="r_check_circle" @click.stop="scope.set" :disable="scope.initialValue === scope.value" />
            </template>
          </q-input>
        </template>
      </q-popup-edit>
  </span>
</template>
<script>


    import {inlineMathHtml} from "src/commons/utils/math-util";

    export default {
        name: "an-inline-math",

        data(){
          return {

            mathLatex : '',
          }
        },
        methods:{
          initMath(mathLatex$){
            this.mathLatex = mathLatex$;
            this.$el.setAttribute('latex', this.mathLatex);
          }

        },
        computed:{

          mathHtml(){
            return  inlineMathHtml(this.mathLatex)
          }
        }
    }
</script>

<style scoped lang="scss">
  .inline-math {
    background-color: $grey-1;
    border: 1px dashed $grey-4;
    border-left: none;
    border-right: none;
  }
</style>
