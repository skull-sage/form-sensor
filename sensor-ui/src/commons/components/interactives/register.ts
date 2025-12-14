import AListTransition from "./a-list-transition.vue";
import AScrollInteract from "./a-scroll-interact.vue";
import ASeqTransition from "./a-seq-transition.vue";
import ASlideTransition from "./a-slide-transition.vue";
import AnInfiniteScroll from "./an-infinite-scroll.vue";






export default (app) => {

  app.component('a-scroll-interact', AScrollInteract);
  app.component('an-infinite-scroll', AnInfiniteScroll);
  app.component('a-slide-transition', ASlideTransition);
  app.component('a-seq-transition', ASeqTransition);
  app.component('a-list-transition', AListTransition);
}
