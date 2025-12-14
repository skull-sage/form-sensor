
export default {

      heading: {
        content: "inline*",
        group: "block",
        defining: true,
        attrs: {level: {default: 3}},
        placeholder: 'write something...',
        parseDOM: [
          {tag: "h2", attrs: {level: 2}},
          {tag: "h3", attrs: {level: 3}}
        ],
        toDOM(node) { return ["h" + node.attrs.level, 0] }
      },
      blockquote: {
        content: "block+",
        group: "block",
        defining: true,
        parseDOM: [{tag: "blockquote"}],
        toDOM() { return ["blockquote", 0] }
      },

      hard_break: {
        inline: true,
        group: "inline",
        selectable: false,
        parseDOM: [{tag: "br"}],
        toDOM() { return ['br'] }
      },


}
