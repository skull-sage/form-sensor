<template>
  <div class="bg-amber-2 q-gutter-x-xs">
   <!-- <a-btn dense key="ul" icon="r_format_list_bulleted"
           @click="$emit('invoke', listMenus.ul.command)" />-->
    <a-btn  dense v-for="item in blockElm" :key="item.name"
            :icon="item.icon"
            :label="item.label" :class="[item.clz]"
            @click="$emit('invoke', item.command)"  />
    <a-btn dense
           icon="r_format_list_bulleted"
           icon-right="r_keyboard_arrow_down">
      <q-menu anchor="top start">
        <q-list  >
          <q-item v-for="(item, index) in listMenus" :key="index"
                  @click="$emit('invoke', item.command)" clickable>
            <q-item-section v-if="item.icon" side><q-icon :name="item.icon" /></q-item-section>
            <q-item-section>{{item.label}}</q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </a-btn>
    <block-math-input :editor-view="editorView" icon="r_functions"/>
    <figure-input :editor-view="editorView" icon="r_image"  />
  </div>
</template>

<script>
import commands from "../config-commands";

import BlockMathInput from "./block-math-input";
import FigureInput from "./figure-input";
export default {
  name: "block-menu",
  props: ['editorView'],
  components: {BlockMathInput, FigureInput},
  data(){
    return {
      blockElm:{
        /*heading_2: {
          label: 'H2',
          clz:'text-weight-bolder',
          command: commands.text.toggleH2
        },*/
        heading_3: {
          icon: 'r_title',
          clz:'text-weight-bolder',
          command:  commands.text.toggleH3

        },
        example: {
          label: 'e.g.',
          clz: 'text-weight-bolder bg-orange-2',
          command: commands.example.insert
      }
      },

      listMenus:[
        {
        command: commands.list.toggleBullet,
        label: 'Bullet List',
        icon: 'r_format_list_bulleted'
        },
        {
          command:  commands.list.toggleOrdered,
          label: '1) 2) 3)'
        },
        {
          command:  commands.list.toggleOrderedLowerRoman,
          label: 'i) ii) iii)'
        },
        {
          command:  commands.list.toggleOrderedUpperRoman,
          label: 'I) II) III)'
        },
        {
          command: commands.list.toggleOrderedUpperAlpha,
          label:"A) B) C)"
        },
        {
          command: commands.list.toggleOrderedLowerAlpha,
          label: 'a) b) c)'
        },
        {
          command: commands.list.toggleOrderedBnNumeric,
          label: '১) ২) ৩)'
        },
        {
          command: commands.list.toggleOrderedBnAlpha,
          label: 'ক) খ) গ)'
        }
      ],

    }
  },


}
</script>

<style scoped>

</style>
