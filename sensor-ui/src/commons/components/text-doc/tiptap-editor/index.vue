<template>
  <editor-content :editor="editor" />
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-3'
import Placeholder from '@tiptap/extension-placeholder'
import StarterKit from '@tiptap/starter-kit'
import {isShallow, isReactive, markRaw, ref, toRaw, shallowReactive} from "vue"


let lastDoc;

export default {
  components: {
    EditorContent,
  },
  emits: ['update:modelValue'],
  data() {
    return {
      editor: null,
    }
  },
  props: {
    modelValue: {
      type: Object,
      default: undefined,
    },
  },
  watch: {
    modelValue(newVal)
    {
       if(newVal !== this.editor.getJSON())
          this.editor.commands.setContent(newVal, false)
       else
         return;
    }
  },
  mounted() {

    this.editor = new Editor({
      content:  this.modelValue,
      extensions: [
        StarterKit,
        Placeholder.configure({
          // Use a placeholder:
          placeholder: 'Write something...'
        })
      ],
      onUpdate: () => {
        // HTML
        //this.$emit('update:modelValue', this.editor.getHTML())
        // JSON
        let docJson = this.editor.getJSON();

        this.$emit('update:modelValue',  markRaw(docJson))
      },
    })
  },

  beforeUnmount() {
    this.editor.destroy()
  },
}
</script>
