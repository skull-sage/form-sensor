
//import commands from '../config-commands'

const  codeDOM = ["code", 0]

export default {

    strong : {
      parseDOM: [{tag: "strong"},
        // This works around a Google Docs misbehavior where
        // pasted content will be inexplicably wrapped in `<b>`
        // tags with a font-weight normal.
        {tag: "b", getAttrs: node => node.style.fontWeight != "normal" && null},
        {style: "font-weight", getAttrs: value => /^(bold(er)?|[5-9]\d{2,})$/.test(value) && null}],
      toDOM() { return ["strong", 0] }
    },
    em: {
      parseDOM: [{tag: "i"}, {tag: "em"}, {style: "font-style=italic"}],
      toDOM() { return ["em", 0] }
    },

    highlight: {
      //
      // color, {primary secondary},
      // underline, {primary, secondary}
      attrs: {style: {default: 'color-primary'}},
      parseDOM: [{tag: "span.bg-teal-1"}],
      toDOM(node) {
        let clz = `highlight ${node.attrs.style}`;
        return ["span", {class : clz}, 0]
      },
    }

}
