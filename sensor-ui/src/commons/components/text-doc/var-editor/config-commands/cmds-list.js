
// to be updated
import {findParentNode} from "../utils";
import {liftListItem, sinkListItem, splitListItem, wrapInList} from "prosemirror-schema-list";


function isList(node, schema) {
  return (node.type === schema.nodes.bullet_list
    || node.type === schema.nodes.ordered_list
    || node.type === schema.nodes.todo_list)
}

function isSameListType(listNode$, reqType$, reqAttrs$)
{
  if(reqType$.name == 'bullet_list')
    return  listNode$.type.name == 'bullet_list'
  else
    return listNode$.type.name == 'ordered_list'
      && listNode$.attrs.type == reqAttrs$.type

}


export  function toggleList(listType, attrs) {


  return (state, dispatch, view) => {
    const { schema, selection } = state
    const { $from, $to } = selection
    const range = $from.blockRange($to)
    let listItem = schema.nodes.list_item;
    if (!range) {
      return false
    }



    const parentList = findParentNode(node => isList(node, schema))(selection)

    if (range.depth >= 1 && parentList && range.depth - parentList.depth <= 1) {
      if (isSameListType(parentList.node, listType, attrs) ) //parentList.node.type === listType
      {
        return liftListItem(listItem)(state, dispatch)
      }

      if (isList(parentList.node, schema) && listType.validContent(parentList.node.content)) {
        const { tr } = state
        tr.setNodeMarkup(parentList.pos, listType, attrs)

        if (dispatch) {
          dispatch(tr)
        }

        return false
      }
    }

    return wrapInList(listType, attrs)(state, dispatch)
  }
}

const olNumeric = {type : 'numeric'}
const olUpperAlpha = {type: 'upper-alpha'};
const olLowerAlpha = {type: 'lower-alpha'};
const olUpperRoman = {type: 'upper-roman'};
const olLowerRoman = {type: 'lower-roman'};
const olBnNumeric  = {type: 'bn-numeric'};
const olBnAlpha    = {type: 'bn-alpha'};

export default {
  toggleOrdered : (state, dispatch) => toggleList(state.schema.nodes.ordered_list, olNumeric)(state, dispatch),
  toggleOrderedUpperAlpha : (state, dispatch) => toggleList(state.schema.nodes.ordered_list, olUpperAlpha)(state, dispatch),
  toggleOrderedLowerAlpha : (state, dispatch) => toggleList(state.schema.nodes.ordered_list, olLowerAlpha)(state, dispatch),
  toggleOrderedUpperRoman : (state, dispatch) => toggleList(state.schema.nodes.ordered_list, olUpperRoman)(state, dispatch),
  toggleOrderedLowerRoman : (state, dispatch) => toggleList(state.schema.nodes.ordered_list, olLowerRoman)(state, dispatch),
  toggleOrderedBnNumeric: (state, dispatch) => toggleList(state.schema.nodes.ordered_list, olBnNumeric)(state, dispatch),
  toggleOrderedBnAlpha: (state, dispatch) => toggleList(state.schema.nodes.ordered_list, olBnAlpha)(state, dispatch),
  toggleBullet: (state, dispatch) => toggleList(state.schema.nodes.bullet_list)(state, dispatch),
  sinkListItem:  (state, dispatch) => sinkListItem(state.schema.nodes.list_item)(state, dispatch),
  liftListItem: (state, dispatch) => liftListItem(state.schema.nodes.list_item)(state, dispatch),
  splitListItem:  (state, dispatch) => splitListItem(state.schema.nodes.list_item)(state, dispatch)
}
