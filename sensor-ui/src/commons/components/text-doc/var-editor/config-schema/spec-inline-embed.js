import katex from "katex";


export default {

  fill_gap: {
      group : 'inline',
      content: 'inline*',
      inline: true,
      atom : true,
      selectable: false,
      parseDOM: [{
        tag: "span.fill-gap.text-blue-grey-3",
        getContent(dom, schema){
          return schema.text('_____'); // 5 underscore
        }
      }],
      toDOM(){
        return ["span", {class: 'fill-gap text-blue-grey-3'}, '_____'] // 5 underscore
      }
    },
  inline_math: {
    group : 'inline',
    content: 'inline*',
    inline: true,
    leaf: true,
    attrs: {latex: {default: "x=5"}},
    atom : true,
    selectable: false,
    parseDOM: [{
      tag: "span.inline-math[latex]",
      getAttrs(dom) {
        let latex = dom.getAttribute("latex");
        return {latex};
      },

    }],
    toDOM(node) {
      let mathHtml = katex.renderToString(node.attrs.latex, {
        throwOnError: false
      });
      return ["span", {class : 'inline-math',
        latex : node.attrs.latex,
        innerHTML: mathHtml
      }];
    }
  },
  ext_link:{
    group : 'inline',
    content: 'inline*',
    inline: true,
    atom : true,
    selectable: false,
    attrs: {href: {default: undefined}, anchorTxt: {default: undefined}},
    parseDOM: [ {tag: "a", getAttrs(dom){
      return {
        href: dom.href,
        anchorTxt: dom.innerText
      }
      }}],
    toDOM(node){
      return ["a", {href: node.attrs.href}, node.attrs.anchorTxt]
    }
  },
}

