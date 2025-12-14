


export default {

   insertBlockMath: (state, dispatch) =>
  {
    let blockMathNode = state.schema.node('block_math')
    let newTr = state.tr.replaceSelectionWith(blockMathNode, false)
    dispatch(newTr);
    return true;
  },

  insertGape: (state, dispatch) =>
  {
    // schema.node() function create a fill gape node
    let fillGapeNode = state.schema.node('fill_gape')
    let newTr = state.tr.replaceSelectionWith(fillGapeNode, false)
     dispatch(newTr);
    return true;
  }
}
