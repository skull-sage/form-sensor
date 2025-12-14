import {Schema} from "prosemirror-model";
import {keymap as keyBindingPluginProvider} from "prosemirror-keymap";
import {buildInputRules} from "./config-inputrules";
import {baseBindingMap, calcKeyBindingMap} from "./config-commands/util-keymap";
import {calcNodeMarkMap} from './config-schema/doc-spec-provider'
import configKeyBinding from './config-commands/config-keybinding'
import SpecParagraph from "./config-schema/spec-paragraph.js";
import SpecBlockText from "./config-schema/spec-block-text.js";
import SpecInlineEmbed from "./config-schema/spec-inline-embed.js";
import SpecBlockExample from "./config-schema/spec-block-example.js";
import SpecBlockList from "./config-schema/spec-block-list.js";
import SpecBlockEmbed from "./config-schema/spec-block-embed.js";
import SpecMarkBasic from "./config-schema/spec-mark-basic.js";

let calcKeyMapAndRuleList = (nodeMap, markMap)=>
{
  let keyBindingMap = baseBindingMap;
  let ruleList = [];

  let allNodeMap = {...nodeMap, ...markMap};

  Object.keys(allNodeMap).forEach(nodeKey => {
    let bindingSpec = configKeyBinding[nodeKey];

    if(bindingSpec)
    {
      //console.log(nodeKey+" => "+Object.keys(bindingSpec))
      calcKeyBindingMap(keyBindingMap, bindingSpec)
    }
  })

  /*specList.forEach(spec => {
    if(spec.keyBindingSpec){
      let bindingSpec = spec.keyBindingSpec(commands);
      calcKeyBindingMap(keyBindingMap, bindingSpec);
    }
    /!* if(spec.ruleSpec)
     {
       spec.ruleSpec.forEach(rule => ruleList.push(rule))
     }*!/
    // calc keyboard key map


  });*/

  return {keyBindingMap, ruleList}
}

const createSchema = (nodeMap,markMap)=>
{
  let docContent = undefined;
  Object.keys(nodeMap).forEach(nodeKey => {
    let node = nodeMap[nodeKey];
    if(node.group == 'block'){
      if(docContent == undefined)
        docContent = 'block';
      else if(docContent == 'block')
        docContent = 'block+'
    }
  });

  return  new Schema({
    nodes: {
      ...nodeMap,
      text: {group : "inline"},
      doc: {content: docContent},
    },
    marks: markMap,
  });
}

/**
 *  basicDoc: {
 *     nodeSpec: [ SpecParagraph,  SpecBlockText, SpecInlineEmbed, SpecBlockExample, SpecBlockList,  SpecBlockEmbed],
 *     markSpec: [SpecMarkBasic]
 *   },
 * */

export default (docSpec)=>{
 /* basicDoc: {
    nodeSpec: [ SpecParagraph,  SpecBlockText, SpecInlineEmbed, SpecBlockExample, SpecBlockList,  SpecBlockEmbed],
      markSpec: [SpecMarkBasic]
  },*/
  let {nodeMap, markMap} =  calcNodeMarkMap(docSpec);

  let {keyBindingMap} = calcKeyMapAndRuleList(nodeMap, markMap);
  let schema = createSchema(nodeMap, markMap);
  let keyBindingPlugin = keyBindingPluginProvider(keyBindingMap);
  let inputRulePlugin = buildInputRules(schema); //{rules: spec.ruleList}
  return {schema, keyBindingPlugin, inputRulePlugin}

};
