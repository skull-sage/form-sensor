import SpecBlockText from './spec-block-text'
import SpecBlockList from './spec-block-list'
import SpecBlockExample from './spec-block-example'
import SpecBlockEmbed from './spec-block-embed'
import SpecInlineEmbed from './spec-inline-embed'
import SpecMarkBasic from './spec-mark-basic'
import SpecParagraph from './spec-paragraph'



let calcMap0 = (nodeMap, aSpec) => {

  Object.keys(aSpec).forEach(key => {
    if(nodeMap[key])
      throw `${key} spec is defined more than once`
    nodeMap[key] = aSpec[key];
  });
}



export const calcNodeMarkMap = ({nodeSpec, markSpec})=>
{
  let nodeMap = {};
  let markMap = {};

  nodeSpec.forEach(aSpec => calcMap0(nodeMap, aSpec));
  markSpec.forEach(aSpec => calcMap0(markMap, aSpec));

  return {nodeMap, markMap}
}




export default {


  basicDoc: {
    nodeSpec: [ SpecParagraph,  SpecBlockText, SpecInlineEmbed, SpecBlockExample, SpecBlockList,  SpecBlockEmbed],
    markSpec: [SpecMarkBasic]
  },
  paragraphOnlyDoc: {
    nodeSpec: [SpecParagraph,  SpecInlineEmbed],
    markSpec: [SpecMarkBasic]
  },


}
