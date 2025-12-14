<template>
  <a-slide-transition fade-only>
  <div ref="menuEl" v-show="menuVisible" @mousedown.prevent.stop=""
    class="fixed  rounded-borders editor-menu">
    <!--<a-btn tertiary dense icon="r_title" />-->
    <format-menu tabindex="0"
                 class="bg-blue-grey-10 text-white shadow-4 shadow-3"
      v-if="menuType == 'FORMAT_MENU'"
      @invoke="invoke($event)"
      :editor-view="editorView"
    />
    <block-menu class="bg-orange-1 text-blue-grey-9 shadow-3"
      :editor-view="editorView"
      @invoke="invoke($event)"
      v-else-if="menuType == 'BLOCK_MENU'"
    />
    <math-menu v-else :editor-view="editorView" />
  </div>
  </a-slide-transition>
</template>
<script>

  import commands from "../config-commands";
  import {findSelectedBlockNode} from "../utils";
  import MathMenu from "./block-math-menu";
  import FormatMenu from "./format-menu";
  import BlockMenu from "./block-menu";

  export default {
    name: "editor-menu",
    components: {BlockMenu, FormatMenu, MathMenu},
    props: ['editorView' ],

    mounted() {


      this.commands = commands;
      //this.update(this.editorView, null);

    },
    data(){
      return {
        menuType: 'BLOCK_MENU', // type: {format_menu, embed_menu}
        menuVisible: false

      }
    },
    methods:
      {

        invoke(command$){
         // console.log('CLICK ON INVOKE')
          this.editorView.focus()
          let {state, dispatch} = this.editorView;
          command$(state, dispatch);
        },

        update(view, lastState) // prosemirror require such method to be existed
        {
          let state = view.state;
          // Don't do anything if the document/selection didn't change
          if (lastState && lastState.doc.eq(state.doc) &&
            lastState.selection.eq(state.selection)) return

          let {doc, selection} = state;
          let nodeList = findSelectedBlockNode(doc, selection);

          if(nodeList.length == 1)
          {

            let {node, pos} = nodeList[0];

            if(node.isAtom)
            {
              if(node.type.name == 'block_math')
              {
                this.showMenu('MATH_MENU');
              }

            }
            else if(node.type.name == 'paragraph' && node.textContent.length == 0)
            {
              this.showBlockMenu('BLOCK_MENU');
            }
            else if(!selection.empty){
              this.showMenu('FORMAT_MENU');
             // this.calcActive();
            }
            else this.hideMenu();
          }
          else{
            this.hideMenu();
          }

        },

        updateOnFocus(){
          let {doc, selection} = this.editorView.state;
          if(!selection.empty)
            return ;
          let nodeList = findSelectedBlockNode(doc, selection);
          if(nodeList.length != 1)
            return;

          let {node, pos} = nodeList[0];
          if(node.type.name == 'paragraph' && node.textContent.length == 0)
          {
            this.showBlockMenu('BLOCK_MENU');
          }

        },

        hideMenu(){

          //this.$el.style.visibility = 'hidden';
         // this.$el.style.opacity = 0;
          this.menuVisible = false;

        },


        showBlockMenu(){
          this.menuType = 'BLOCK_MENU';
          let {from, to} = this.editorView.state.selection;
          this.menuVisible = true;
          this.$nextTick(()=>{
            let menuEl = this.$refs.menuEl;
            let start = this.editorView.coordsAtPos(from);
            let box = menuEl.getBoundingClientRect();
            menuEl.style.left = (start.left )+'px';
            menuEl.style.top = (start.top - box.height - 4)+'px';

          })
        },

        showMenu( menuType$ )
        {
          this.menuType = menuType$;
          this.menuVisible = true;
          this.$nextTick(() => {
            let menuEl = this.$refs.menuEl;

            let {from, to} = this.editorView.state.selection;
            let start = this.editorView.coordsAtPos(from);
            let end = this.editorView.coordsAtPos(to);
            let box = menuEl.getBoundingClientRect();
            //let editorBox = this.editorView.dom.getBoundingClientRect();
            let left = (start.left + end.left - box.width) / 2  ;

            let {innerWidth: vpWidth} = window;
            if(left < 4)
              left = 4;
            else if(left + box.width > vpWidth)
            {
              left = vpWidth - box.width;
            }

            menuEl.style.left =  left + "px"; //editorBox.left+"px";//
            menuEl.style.top =  start.top - box.height - 8  + "px";
          })




        },
       /* calcActive(){
          for (const [key, value] of Object.entries(this.formatMenus)) {
            value.active = false;
          }
          let parent = this.editorView.state.selection.$from.parent;
          if(parent.type.name == "heading")
          {
            let name = parent.type.name + "_" + parent.attrs.level;
            this.formatMenus[name].active = true;
          }


        },*/
        destroy() { this.$destroy();}
      }
  }
</script>

<style scoped lang="scss">
  .menu-icon
  {
    color: white;
  }
  .editor-menu{
   // visibility: hidden;
    display: inline-block;
    transition: opacity  300ms;
    z-index: $z-tooltip;
  }
</style>
