
import AnInput from "src/commons/components/forms/an-input.vue";
import AField from "src/commons/components/forms/a-field.vue";
import ADaTimeInput from "src/commons/components/forms/a-datime-input.vue";
import AnImageInput from "src/commons/components/forms/an-image-input.vue";

export default (app)=>
{

//=====  form input registration
  app.component('an-input', AnInput);
  app.component('a-field', AField);
// app.component('a-doc-input', ADocInput);
  app.component('a-datime-input', ADaTimeInput)
  app.component('an-image-input', AnImageInput);
}
