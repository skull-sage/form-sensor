
import commands from './index'

export default {
  strong : {
    "Mod-b": commands.text.markStrong,
    "Mod-B": commands.text.markStrong,
  },
  em:{
    "Mod-i": commands.text.markEm,
    "Mod-I": commands.text.markEm
  },
  hard_break:{
    "Shift-Enter": commands.text.heardBreak
  },
  block_quote:{
    "Ctrl->": commands.text.insertBlockQuote,
  },
  example:{
    "Delete": commands.example.delete,
    "Enter": commands.example.createParagraphNear
  },
  list_item:{
    "Tab":  commands.list.sinkListItem,
    "Shift-Tab": commands.list.liftListItem,
    "Enter":  commands.list.splitListItem
  },


}
