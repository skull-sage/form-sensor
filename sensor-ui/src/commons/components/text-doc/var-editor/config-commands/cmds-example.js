import {findParentNodeOfType} from "../utils";
import {NodeSelection, TextSelection} from "prosemirror-state";


export default {
  insert(state, dispatch){
    let exampleJson = {
      type: 'example',
      content: [
        {type: 'example_caption', content: [ ]},
        {type: 'example_content', content: [ ]},
        {type: 'example_explanation', content: [ ]},

      ]
    }

    let exampleNode = state.schema.nodeFromJSON(exampleJson);
    let {selection, tr} = state;
    tr = tr.replaceSelectionWith(exampleNode);
    //tr = tr.setSelection(selection)
    dispatch(tr);
    return true;
  },
  delete(state, dispatch)
  {
    let exampleBlock = findParentNodeOfType(state.schema.nodes.example)(state.selection);
    if(!exampleBlock) return  false;
    let {pos, start, node} = exampleBlock;

    let nodeSelection = NodeSelection.create(state.doc, pos);
    let _tr =  state.tr.setSelection(nodeSelection);
    _tr = _tr.deleteSelection();
    dispatch(_tr);
    return true;
  },
  createParagraphNear(state, dispatch) {
    //debugger;
    let exampleBlock = findParentNodeOfType(state.schema.nodes.example)(state.selection);
    if(!exampleBlock) return  false;
    let {pos, start, node} = exampleBlock;
    //let _tr = state.tr.setSelection(TextSelection.create(state.doc, start+node.size()))
    let pNode = state.schema.nodeFromJSON({type:'paragraph'});
    let nextPos = pos + node.nodeSize;
    let _tr = state.tr.insert(nextPos, pNode);
    _tr = _tr.setSelection(NodeSelection.create(_tr.doc, nextPos))
    dispatch(_tr);

    return true;
  }
}
