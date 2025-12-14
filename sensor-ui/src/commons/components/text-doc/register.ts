import DocBasic from "./var-editor/doc-basic.vue";
import DocEditor from "./var-editor/doc-editor.vue";
import AText from "./a-text.vue";
import ATitle from "./a-title.vue";
import ACaption from "./a-caption.vue";

//import 'katex/dist/katex.min.css';

export default (app) => {

  app.component('doc-basic', DocBasic);
  app.component('a-text', AText);
  app.component('a-title', ATitle);
  app.component('a-caption', ACaption);
}
