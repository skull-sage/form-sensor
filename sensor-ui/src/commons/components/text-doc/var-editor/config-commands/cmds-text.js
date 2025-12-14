import {findParentNodeOfType} from "../utils";
import {setBlockType, toggleMark, wrapIn} from "prosemirror-commands";

function markApplies(doc, ranges, type) {

  for (let i = 0; i < ranges.length; i++) {
    let {$from, $to} = ranges[i]
    let can = $from.depth == 0 ? doc.type.allowsMarkType(type) : false
    doc.nodesBetween($from.pos, $to.pos, node => {
      if (can) return false
      can = node.inlineContent && node.type.allowsMarkType(type)
    })
    if (can) return true
  }
  return false
}

function toggleMark0(markType, attrs) {
  return function(state, dispatch) {
    let {empty, $cursor, ranges} = state.selection
    if ((empty && !$cursor) || !markApplies(state.doc, ranges, markType)) return false
    if (dispatch) {
      if ($cursor) {
        if (markType.isInSet(state.storedMarks || $cursor.marks()))
          dispatch(state.tr.removeStoredMark(markType))
        else
          dispatch(state.tr.addStoredMark(markType.create(attrs)))
      } else {
        let has = false, tr = state.tr
        for (let i = 0; !has && i < ranges.length; i++) {
          let {$from, $to} = ranges[i]
          has = state.doc.rangeHasMark($from.pos, $to.pos, markType)
        }
        for (let i = 0; i < ranges.length; i++) {
          let {$from, $to} = ranges[i]
          if (has) {
            tr.removeMark($from.pos, $to.pos, markType)
          } else {
            let from = $from.pos, to = $to.pos, start = $from.nodeAfter, end = $to.nodeBefore
            let spaceStart = start && start.isText ? /^\s*/.exec(start.text)[0].length : 0
            let spaceEnd = end && end.isText ? /\s*$/.exec(end.text)[0].length : 0
            if (from + spaceStart < to) { from += spaceStart; to -= spaceEnd }
            tr.addMark(from, to, markType.create(attrs))
          }
        }
        dispatch(tr.scrollIntoView())
      }
    }
    return true
  }
}

const toggleHeadingCmdProvider = (level$) => {
  return (state, dispatch) => {
    let headingType = state.schema.nodes.heading;
    if(!headingType) return false;
    let heading = findParentNodeOfType(headingType)(state.selection);
    if(heading && heading.node.attrs.level == level$)
      return setBlockType(state.schema.nodes.paragraph)(state, dispatch);
    else
      return setBlockType(state.schema.nodes.heading, {level: level$})(state, dispatch);
  }

}
export default {
  toggleH2 : toggleHeadingCmdProvider(2),
  toggleH3: toggleHeadingCmdProvider(3),
  markStrong : (state, dispatch) => toggleMark(state.schema.marks.strong)(state, dispatch),
  markEm: (state, dispatch) => toggleMark(state.schema.marks.em)(state, dispatch),
  colorPrimary: (state, dispatch) => toggleMark(state.schema.marks.highlight, {style: 'color-primary'})(state, dispatch),
  colorSecondary: (state, dispatch) => toggleMark(state.schema.marks.highlight, {style: 'color-secondary'})(state, dispatch),
  underlinePrimary: (state, dispatch) => toggleMark(state.schema.marks.highlight, {style: 'underline-primary'})(state, dispatch),
  underlineSecondary: (state, dispatch) => toggleMark(state.schema.marks.highlight, {style: 'underline-secondary'})(state, dispatch),
  heardBreak: (state, dispatch) => {
    let br = state.schema.nodes.hard_break;
    if(br)
    {
      dispatch(state.tr.replaceSelectionWith(br.create()).scrollIntoView())
      return true
    }
  },
  insertBlockQuote:(state, dispatch) => wrapIn(state.schema.nodes.blockquote)(state, dispatch)

}
