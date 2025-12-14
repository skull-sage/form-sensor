export default {

    paragraph: {
      group: 'block',
      content: 'inline*',
      parseDOM: [{tag: "p"}],
      placeholder: 'write something...',
      toDOM() { return ["p", 0] }
    }

}
