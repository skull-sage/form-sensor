import Vue from "vue";
import AnInlineMath from './an-inline-math'
import {NodeSelection, TextSelection, Selection} from "prosemirror-state";
import {removeNodeAtPos} from "../utils/helpers";

let InlineMathV = Vue.extend(AnInlineMath)

export default class NVInlineMath {
  constructor(node$, view$, getPos$) {

    this.mathVM = new InlineMathV()
    this.mathVM.$mount() // pass nothing
    this.dom =  this.mathVM.$el;
    this.mathVM.initMath(node$.attrs.latex);

    this.mathVM.$on('input', (data$)=> {
      let viewState = view$.state;
      let posTo = viewState.selection.to;

      if(!data$ || data$.length == 0)
      {
        let _tr = removeNodeAtPos(getPos$())(viewState.tr);
        view$.dispatch(_tr);

        return;
      }
      let copy = node$.copy();
      copy.attrs = {latex : data$};
      let nodeSelection = NodeSelection.create(viewState.doc, getPos$());
      let _tr =  viewState.tr.setSelection(nodeSelection);
       _tr = _tr.replaceSelectionWith(copy, false);
       view$.dispatch(_tr);
    })

  }

 /* selectNode(){
    this.mathVM.showEditor(this.docNode.attrs.latex);
  }

  deselectNode(){
    console.log('NOT DESELECTING ?');
    this.mathVM.hideEditor();
  }*/
 }
