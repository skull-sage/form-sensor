import registerLayouts from "./layouts/register";
import registerElements from "./elements/register";
import registerInputs from "./forms/register";
import registerTextDoc from "./text-doc/register";


export default (app) => {

  registerLayouts(app);
  registerElements(app);
  registerTextDoc(app);
  registerInputs(app);

}

