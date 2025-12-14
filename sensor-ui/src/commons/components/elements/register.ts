
import ASpinner from "./a-spinner.vue";
import ARoute from "./a-route.vue";
import ANavItem from "./a-nav-item.vue";
import ATabs from "./a-tabs.vue";
import ADropDown from "./a-dropdown.vue";
import AProgress from "./a-progress.vue";
import AWarning from "./a-warning.vue";
import ADaTime from "./a-datime.vue";
import ABtn from "./a-btn.vue";
import GradientBtn from "./gradient-btn.vue";


export default (app): void => {
  app.component('a-btn', ABtn);
  app.component('gradient-btn', GradientBtn);
  app.component('a-spinner', ASpinner);
  app.component('a-route', ARoute);
  app.component('a-nav-item', ANavItem);
  app.component('a-tabs', ATabs);


  app.component('a-dropdown', ADropDown);
  app.component('a-progress', AProgress);
  app.component('a-warning', AWarning);
  app.component('a-datime', ADaTime);

}
