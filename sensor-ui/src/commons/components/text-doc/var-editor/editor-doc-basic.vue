<template>
  <div class="bg-white  relative-position">
    <div ref="editor" class="editor-doc-basic"></div>
    <editor-menu
      :editor-view="editorView"
      ref="editorMenu"
      :blob-ref="blobRef" />
  </div>
</template>
<script>

 // import {basicSchema, textSchema} from './config-schema/schema-provider'
  import {EditorState} from "prosemirror-state"
  import {DOMParser} from "prosemirror-model";
  import {EditorView} from "prosemirror-view"
  import {history} from "prosemirror-history"
  import DocSpecProvider from "./config-schema/doc-spec-provider"
  import buildSchema from './schema-builder'
  import menuBuilder from './plugins/menu-selection-plugin'
  import nodeViewRegistry from './config-nodeview'
  import {htmlStrToDom} from "src/commons/utils/dom-util";
  import EditorMenu from "./editor-menus/editor-menu";

  export default {
    name: "editor-doc-basic",
    components: {EditorMenu},
    props : {
        value:  [String, Object],

        contentType: {
          type: String,
          default: 'json'
        },
        placeholder:{
          type: String,
          default: 'Start writing...'
        },

        simple: Boolean,
        singleParagraph: Boolean,

        blobRef: {
          type: Array,
          default: undefined
        },
    },
    data(){
      return {
        editorView: undefined
      }
    },
    mounted() {
      this.initialize(this.value);
    },



    methods:{
      clearDoc(){
        let {state} = this.editorView;
        let _tr = state.tr.delete(0, state.doc.content.size);
        this.editorView.dispatch(_tr);

        //this.$emit('input', undefined);
        //this.initialize(undefined);
      },
      initialize(initialVal$){
        let editorElm =  this.$refs['editor'];

        let docSpec = this.singleParagraph ? DocSpecProvider.paragraphOnlyDoc: DocSpecProvider.basicDoc;
        let {schema, keyBindingPlugin, inputRulePlugin} = buildSchema(docSpec);

        let pluginList = [
          history(),
          inputRulePlugin,
          keyBindingPlugin,
          menuBuilder(this.$refs.editorMenu)
         // buildInputRules(schema),
         // keymap(buildKeymap(schema)),
         // keymap(baseKeymap), // or text
        ];


        let initState = {
          doc : this.deriveDoc(schema, initialVal$),
          schema : schema,
          plugins: pluginList,
        }


        let state = EditorState.create(initState);

        let $vm = this;
        let view = new EditorView(editorElm,
          {
            state: recordingState,
            nodeViews: nodeViewRegistry,
            dispatchTransaction(transaction) {
              let {docChanged} = transaction;

              let newState = view.state.apply(transaction);

              view.updateState(newState);
              //let stateJson = newState.toJSON();
              // delete stateJson['selection'];
              if(docChanged)
              {
                $vm.emitChanges(newState.doc)
              }


            }
          }
        );

        this.editorView = view;
        this.editorView.blobRef = this.blobRef;
      },
      deriveDoc(schema$, initialVal$){
        if(initialVal$ === undefined)
          return undefined;

        if(initialVal$.type == 'html')
        {
          let domElm = htmlStrToDom(initialVal$.content);
          return DOMParser.fromSchema(schema$).parse(domElm);
        }
        else //if(initialVal$ && JSON.stringify(initialVal$) == '{}')
        {

          let docJson = initialVal$.doc ? initialVal$.doc : initialVal$;
          if(docJson.type == 'doc')
            return schema$.nodeFromJSON(docJson)
          else
            return undefined;
        }
      },
      emitChanges(doc$) {
        let hasContent = false;

        doc$.content.forEach(node => {
         // console.log(`${node.type} has content ${node.content.length}`)
          if(node.isTextblock && node.content)
          {
            if(node.textContent.trim().length > 0)
              hasContent = true;
            else{

              node.content.forEach(inlineNode => {

                if(inlineNode.isText == false && inlineNode.isAtom)
                  hasContent = true;
              })
            }

          }
          else {
            hasContent = true;
          }
        })

        if (hasContent)
          this.$emit('input', doc$.toJSON());
        else {
          this.$emit('input', undefined);
        }
      }
    }

  }
</script>

<style scoped lang="scss">

.editor-doc-basic :deep(.ProseMirror) {

    min-height: $space-base * 2;

    &:focus{
      outline: none;
      p.empty-doc::before{
        content: none;
      }

    }

    .empty-doc{
      color: $grey-5;
    }
    /*p.empty-doc::before{
      color: $grey-5;
      content: 'Start Writing...';
    }*/

    .has-focus{
      outline: 1px dashed $indigo-3;
    }

    .has-atom-focus{
      outline: 2px solid $teal-4;
    }



  }
</style>
