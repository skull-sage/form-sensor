
import {NodeSelection, Plugin} from "prosemirror-state"
import {findBlockNodes, findSelectedBlockNode} from "../utils";
import {Decoration, DecorationSet} from "prosemirror-view";




export default   (menuVM$) =>
{
  return new Plugin({

    view(editorView$){

      return menuVM$;

      //return new SelectionCapture(editorView);
    },
    props: {
      handleDOMEvents:{
        focus : (view, $event) => {
           menuVM$.updateOnFocus();


        },
        blur : (view, $event) =>  {
          if(menuVM$.$refs.menuEl != document.activeElement)
          {
            //console.log(document.activeElement)
            menuVM$.hideMenu()
          }
        }
      },


      decorations: ({ doc, plugins, selection }) => {

        const { anchor } = selection
        const decorationList = [];

        /*let {from, node:selectedNode} = selection;
        if(selectedNode && selectedNode.isAtom && selectedNode.isBlock){
          const atomFocusDeco = Decoration.node(from, from + selectedNode.nodeSize, {
            class: 'has-atom-focus',
          });
          decorationList.push(atomFocusDeco)
        }*/

        findBlockNodes(doc, true)
          .forEach(({node, pos}) => {

            if(node.isTextblock && node.content.size == 0)
            {
              let {placeholder} = node.type.spec;
              if(placeholder){
                let emptyWidget = Decoration.widget(pos+1, document.createTextNode(placeholder))
                let emptyDeco = Decoration.node(pos, pos + node.nodeSize, {class: 'empty-doc'})
                decorationList.push(emptyDeco, emptyWidget);
              }

            }
        })

        return DecorationSet.create(doc, decorationList)

      },
    },

  })
}

/*export default*/
