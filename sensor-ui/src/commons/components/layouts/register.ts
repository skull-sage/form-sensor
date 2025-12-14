import ActivityContainer from './activity/activity-container.vue'
import ADrawer from './activity/a-drawer.vue'
import BtnDrawerOpen from './activity/btn-drawer-open.vue'
import BtnDrawerClose from './activity/btn-drawer-close.vue'

import ASegment from './activity/a-segment.vue'
import FVContainer from './activity/fv-container.vue'
import ASection from "./activity/a-section.vue";
import AFlexApart from './a-flex-apart.vue'

import AScrollArea from './a-scroll-area.vue'
import APage from './a-page.vue'
import MultiSectionPage from './a-sensor-page.vue'
import AHlSection from './a-hl-section.vue'
import ActionDialog from './action-dialog.vue'




export default (app) => {


  app.component('activity-container', ActivityContainer);
  app.component('a-drawer', ADrawer)
  app.component('btn-drawer-open', BtnDrawerOpen)
  app.component('btn-drawer-close', BtnDrawerClose)
  app.component('a-page', APage);
  app.component('multi-section-page', MultiSectionPage)

  app.component('a-segment', ASegment);
  app.component('a-section', ASection);
  app.component('fv-container', FVContainer);
  app.component('a-flex-apart', AFlexApart);

  app.component('a-scroll-area', AScrollArea);
  app.component('action-dialog', ActionDialog);

  //hero sections
  app.component('a-hl-section', AHlSection)
}
