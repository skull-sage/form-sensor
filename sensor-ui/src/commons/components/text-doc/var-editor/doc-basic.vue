
<script>
import   SpecProvider from './config-schema/doc-spec-provider'
import {calcNodeMarkMap} from './config-schema/doc-spec-provider'

export default {
  name: "doc-basic",
  props: ['value'],
  data: // making non reactive
  {
    nodeSpecMap : undefined,
    markSpecMap : undefined
  },
  render(hElm, context) {
    if(!this.value) return ;
    let docJson = this.value.doc ? this.value.doc : this.value;
    if(docJson.type == 'html')
      return hElm('div', {class: 'doc-basic', domProps: {innerHTML : docJson.content}});
    else // type == 'doc'
    {
      let {nodeMap, markMap} = calcNodeMarkMap(SpecProvider.basicDoc);
      this.nodeSpecMap = nodeMap;
      this.markSpecMap = markMap;
      return this.renderDoc(docJson, hElm);
    }
  },
  methods:{
    renderDoc(doc$, hElm$){
      let vNodeList = [];
      doc$.content.forEach(node => {
        let vNode = this.renderNode(node, hElm$);
        if(vNode != undefined)
          vNodeList.push(vNode);
      })
      return  hElm$('div', {class: 'doc-basic'}, vNodeList);
    },
    renderNode(node$, hElm$)
    {

      let spec, domSpec;
      try{

        if(node$.type=='text')
          return this.createText(node$, hElm$)
        else if(node$.type == 'hard_break')
          return hElm$('br');

        spec = this.nodeSpecMap[node$.type];
        domSpec = spec.toDOM(node$); // returns array [tag, attr, 0] or [tag, 0]
        if(spec.atom == true){
            return this.createAtom(node$, domSpec, hElm$)
        }

        let vNodeList = [];
        if(node$.content == undefined)
          return undefined;
        node$.content.forEach(node => {

            let vNode = this.renderNode(node, hElm$);
            vNodeList.push(vNode);
        });

        if(domSpec.length == 3)
          return hElm$(domSpec[0], domSpec[1], vNodeList);
        else
          return hElm$(domSpec[0], vNodeList)
      }catch (err) {
        console.log(node$);
        console.log(spec)
        console.log(err)
      }

    },

    createAtom(node$, domSpec$, hElm$){
       if(node$.type == 'inline_math' || node$.type=='block_math')
       {
           let innerHTML = domSpec$[1].innerHTML;
           let clz = domSpec$[1].class;
           return hElm$(domSpec$[0],  {class: clz, domProps: {innerHTML : innerHTML}});

       }
       else if(node$.type == 'ext_link'){
         return  hElm$(domSpec$[0], {domProps: domSpec$[1]}, domSpec$[2])
       }
       else if(node$.type == 'figure')
         return this.createFigure(node$, hElm$);
       else if(node$.type == 'fill_gap'){
          return hElm$(domSpec$[0], domSpec$[1], domSpec$[2])
       }

    },

    createBlockMath(){

    },

    createFigure(docNode$, hElm$){
      let {cdn, key} = docNode$.attrs.blob;
      let figSrc = `${cdn}/${key}`;
      //console.log('Figure Src: '+figSrc)
      let imgDom = hElm$('img', {
        attrs: {src: figSrc}, // src needs to be nested as attrs
        class: 'img-responsive-x'
      });
      return hElm$('figure', {class: 'flex justify-center'}, [imgDom]);

    },

    createText(txtNode$, hElm$){
       let {marks} = txtNode$;
       if(!marks)
         return txtNode$.text;

       let mark = marks[0];

        let spec = this.markSpecMap[mark.type]
        let domSpec = spec.toDOM(mark);
        if(domSpec.length == 3)
        {
          return hElm$(domSpec[0], domSpec[1], txtNode$.text);
        }
        else if(domSpec.length == 2){
          return hElm$(domSpec[0], txtNode$.text)
        }

    }
  }
}
</script>
