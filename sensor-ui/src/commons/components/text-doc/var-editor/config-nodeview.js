//import FigureNV from "../util-pmirror/a-figure/nv-figure";
import NVInlineMath from './node-views/nv-inline-math'
import NvExtLink from "./node-views/nv-ext-link";
export default {
  inline_math(node, view, getPos){
    return new NVInlineMath(node, view, getPos)
  },
  ext_link(node, view, getPos){
    return new NvExtLink(node, view, getPos)
  }
}
