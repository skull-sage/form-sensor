import {redo, undo} from "prosemirror-history";
import {undoInputRule} from "prosemirror-inputrules";
import {joinDown, joinUp, lift, selectParentNode, baseKeymap,  exitCode} from "prosemirror-commands";

let chainTwoCmd = (first$, scnd$)=>{
  return (state, dispatch) =>{
    if(first$(state, dispatch))return true;
    else return scnd$(state, dispatch)
  }
}

let calcKeyBindingMap = (keyBindingMap, aSpec)=>
{
  Object.keys(aSpec).forEach(key =>{
    let specCmd = aSpec[key];
    let existingCmd = keyBindingMap[key];
    if(existingCmd)
      keyBindingMap[key] = chainTwoCmd(specCmd, existingCmd);
    else
      keyBindingMap[key] = specCmd
  })
}


let commonKeyMap = {
  "Mod-z":undo,
  "Shift-Mod-z": redo,
  "Backspace": undoInputRule,
  "Alt-ArrowUp": joinUp,
  "Alt-ArrowDown": joinDown,
  "Mod-BracketLeft": lift,
  "Escape": selectParentNode,
  "Shift-Enter": exitCode,
}

let baseBindingMap = {};

calcKeyBindingMap(baseBindingMap, baseKeymap);
calcKeyBindingMap(baseBindingMap, commonKeyMap);

export {calcKeyBindingMap, chainTwoCmd, baseBindingMap}
