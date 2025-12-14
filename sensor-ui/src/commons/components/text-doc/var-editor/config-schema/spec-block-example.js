

export default {
    
    example: {
      content: "example_caption example_content example_explanation",
      group: "block",
      defining: true,
      parseDOM: [{tag: "div.example"}],
      toDOM() {
        return  ["div", {class : 'example'},   0]
      }
    },
    example_caption:{
      content: "text*",
      marks: "",
      group: 'block',
      defining: true,
      parseDOM: [{tag: "div.example-caption"}],
      placeholder: 'example caption',
      toDOM(node) {
          return  ["div", {class : 'example-caption'},  0]
      }
    },
    example_content:{
      group: 'block',
      content: 'inline*',
      parseDOM: [{tag: "p.example-content"}],
      placeholder: 'example content',
      toDOM() {
        return  ["p", {class : 'example-content'},  0]
      }
    },
    example_explanation:{
      content: "inline*",
      group: 'block',
      parseDOM: [{tag: "p.example-explanation"}],
      placeholder: 'write explanation (optional)',
      toDOM() {
        return  ["p", {class : 'example-explanation'},  0]
      }
    }
}
