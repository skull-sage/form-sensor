<template>
  <div class="q-px-xs">
    <a-btn
           tertiary dense  v-for="(item, itemKey) in formatMenus"
           :key="itemKey"
           size="14px"
           :icon="item.icon"    :label="item.label"
           class="text-body1 " :class="[item.clz]"
           @click="$emit('invoke', item.command)"

    />
    <link-input :editor-view="editorView" />
    <a-btn icon="r_format_paint" icon-right="r_keyboard_arrow_down">
      <q-menu auto-close>
        <div class=" bg-grey-1 q-px-xs q-gutter-xs">
        <a-btn no-caps dense
               v-for="(item, itemKey) in hlMenus"
               :key="itemKey" @click="$emit('invoke', item.command)"
        >
          <span :class="item.clz">{{item.label}}</span>
        </a-btn>
        </div>
      </q-menu>
    </a-btn>
  </div>
</template>

<script>
import commands from "../config-commands";
import LinkInput from "./link-input";

export default {
  name: "format-menu",
  components: {LinkInput},
  props: ['editorView'],
  data(){
    return {

      formatMenus: {
        bold: {
          command: commands.text.markStrong,
          icon:'r_format_bold',
        },
        italic: {

          command: commands.text.markEm,
          icon: 'r_format_italic',
        },
      },
      hlMenus:{
        colorPrimary: {
           label: 'Wordy',
           clz: 'highlight color-primary',
           command: commands.text.colorPrimary
        },
        colorSecondary:{
          label: 'Wordy',
          clz: 'highlight color-secondary',
          command: commands.text.colorSecondary
        },
        underlinePrimary:{
          label: 'Wordy',
          clz: 'highlight underline-primary',
          command: commands.text.underlinePrimary
        },
        underlineSecondary:{
          label: 'Wordy',
          clz: 'highlight underline-secondary',
          command: commands.text.underlineSecondary
        }
      }
    }
  },
  methods:{
    initLink(){
      this.editorView.state.tr.replaceSelectionWith()
    }
  }
}
</script>

<style scoped>

</style>
