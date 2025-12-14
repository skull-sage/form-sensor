<template>
    <a-list-transition
      class=" bg-grey-2 q-pa-xs q-gutter-xs">
        <div class="row shadow-2  list-complete-item"
             v-for="(data, index) in dataList" :key="data[keyName]"
             :class="[selectedIdx == index ? selectionContainerClass : '']">
          <div class="col-auto flex items-baseline">
            <a-btn  dense tertiary  icon="r_drag_indicator"
                    @click="toggleSelect(index)"
                    v-show="selectedIdx === undefined || selectedIdx == index"
                    :class="[ selectedIdx == index ? selectionDragClass : 'text-blue-grey-5']"
            />
            <div v-show="selectedIdx !== undefined && selectedIdx != index"
                 class="column items-end">
              <a-btn dense neutral tertiary icon="r_vertical_align_top" class="text-cyan-7"
                     @click="placeAt(index)"/>
              <a-btn  dense neutral tertiary icon="r_vertical_align_bottom" class="text-teal-7"
                     @click="placeAt(index + 1 )" />

            </div>
          </div>
          <div class="col text-black">
            <slot :item="data" :index="index">
              {{data}}
            </slot>
          </div>
        </div>
    </a-list-transition>
</template>

<script>
    export default {
        name: "bucket-list",
        props: {
          value : Array,
          keyName: {
            type: String,
            default: 'id'
          },
          selectionColor: {
            type : String,
            default: 'indigo-13'
          }
        },
       watch:{
          'value.length': {
            handler: 'wrapList',
            immediate: true,

          },

       },
      data(){
          return {
            dataList: null,
            //selected : false,
            selectedIdx: undefined,
          }
        },
        computed:
          {
            selectionContainerClass(){
              return `text-${this.selectionColor} drag-highlight`
            },

            selectionDragClass(){
              return `text-${this.selectionColor}`
            },


          },
        methods:{

          toggleSelect(idx$){
            if(this.selectedIdx == idx$)
            {
              this.selectedIdx = undefined;
            }
            else
              this.selectedIdx = idx$;

          },
          wrapList(new$, old$){

              let wrapList = [];
              this.value.forEach((item, index) => {
                wrapList.push(item);
              });
              this.dataList = wrapList;

          },

          placeAt(idx$)
          {
              let selected = this.dataList[this.selectedIdx];
              this.dataList.splice(this.selectedIdx, 1);
              this.dataList.splice(idx$, 0, selected);

              this.$nextTick(()=>{
                this.selectedIdx = undefined;
                this.$emit("input", this.dataList)
              });
          },



        }
    }
</script>

<style scoped lang="scss">
  .drag-highlight
  {
    box-shadow: 0 0px 0px 2px currentColor;

  }


</style>
