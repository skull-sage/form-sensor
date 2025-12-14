import {blockMathHtml} from "src/commons/utils/math-util";
import {htmlStrToDom} from "src/commons/utils/dom-util";

export  default {

    block_math: {
      group : 'block',
      content: 'block*',

      attrs: {latex: {default: ""}},
      atom: true,
      selectable: true,

      parseDOM: [{
        tag: "div.block-math[latex]",
        getAttrs(dom) {
          let latex = dom.getAttribute("latex");
          return {latex};
        },

      }],
      toDOM(node) {
        let mathHtml =  blockMathHtml(node.attrs.latex);
        let mathDom = htmlStrToDom(mathHtml);
        return ["div", {class : 'block-math' , contentEditable: false,
          latex : node.attrs.latex, innerHTML: mathHtml}, mathDom];
      }
    },
    figure: {
      group : 'block',
      content: 'block*',
      attrs: {
        src:  {default: ''},
        blob: {default : {cdn: '', key: ''}}
      },
      atom: true,
      selectable: true,
      parseDOM: [{
        tag: 'figure',
        getAttrs(dom){
          let img = dom.querySelector("img")
          return {src: img && img.parentNode == dom ? img.src : "default_image.jpg"}
        }
      }],
      toDOM(node){
        let {cdn, key} = node.attrs.blob;
        let figSrc = `${cdn}/${key}`;

        return ['figure',
          {class: 'flex justify-center'},
          ["img",
            {
              src: figSrc,
              class: 'img-responsive-x'
            }
          ]
        ]
      }
    },


}
