

export default {

    // An ordered list [node spec](#model.NodeSpec). Has a single
    // attribute, `order`, which determines the number at which the list
    // starts counting, and defaults to 1. Represented as an `<ol>`
    // element.
    ordered_list : {
      group : 'block',
      content: "list_item+",
      attrs: {order: {default: 1}, type: {default: 'numeric'}},
      parseDOM: [{tag: "ol", getAttrs: function(dom) {
          return {
            order: dom.hasAttribute("start") ? +dom.getAttribute("start") : 1,
            type: dom.hasAttribute('type') ? + dom.getAttribute("type") : 'numeric'
          }
        }}],
      toDOM: function toDOM(node) {
        return  ["ol", {type: node.attrs.type}, 0]
      }
    },
  // A bullet list node spec, represented in the DOM as `<ul>`.
    bullet_list : {
      group : 'block',
      content: "list_item+",
      parseDOM: [{tag: "ul"}],
      toDOM: function toDOM() { return ["ul", 0] }
    },
    // A list item (`<li>`) spec.
    list_item:{
      content : "paragraph+",
      parseDOM: [{tag: "li"}],
      toDOM: function toDOM() { return ["li", 0] },
      defining: true
    }


}

