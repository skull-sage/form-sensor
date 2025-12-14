import Vue from "vue";
import AnExtLink from './an-ext-link'
import {NodeSelection, TextSelection, Selection} from "prosemirror-state";
import {removeNodeAtPos} from "../utils/helpers";

let AnExtLinkVM = Vue.extend(AnExtLink)

export default class NvExtLink {
  constructor(node$, view$, getPos$) {

    this.linkVM = new AnExtLinkVM()
    this.linkVM.$mount() // pass nothing
    this.dom =  this.linkVM.$el;
    this.linkVM.initData(node$.attrs);

    this.linkVM.$on('input', (data$)=> {
      let viewState = view$.state;
      let posTo = viewState.selection.to;

      let node = {
        type: 'ext_link',
        attrs: {href: data$.href, anchorTxt: data$.anchorTxt},
      }
      let nodeSelection = NodeSelection.create(viewState.doc, getPos$());
      let _tr =  viewState.tr.setSelection(nodeSelection);
      _tr = _tr.replaceSelectionWith(node);
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
