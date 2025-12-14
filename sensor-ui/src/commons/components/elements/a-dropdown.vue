<template>
  <q-btn-dropdown auto-close stretch flat :label="selectedLabel">
    <q-list link>
      <q-item v-if="defLabel" clickable :key="0" @click.native="selectItem()">
        <q-item-section>{{defLabel}}</q-item-section>
        <q-separator />
      </q-item>
      <q-item clickable
              v-for="item in itemList"
              :key="item.id"
              @click.native="selectItem(item)">
        <q-item-section>{{item[labelProp]}}</q-item-section>
        <q-separator />
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
    export default {
        name: "a-dropdown",
      props: ['itemList', 'value', 'labelProp', 'defaultLabel', 'valueProp'],
      data(){
        return {
          selectedItem : this.value
        };
      },
      computed : {
          selectedLabel(){
            if(this.selectedItem == undefined)
              return this.defLabel;
            else  return this.selectedItem[this.labelProp];

          }
      },
      methods:{
        selectItem(item){
          this.selectedItem = item;
          if(this.valueProp)
            this.$emit("input", this.selectedItem[this.valueProp]);
          else this.$emit("input", this.selectedItem);
        },
        computed:{
            label(){

            }
        }
      }
    }
</script>

<style scoped>

</style>
