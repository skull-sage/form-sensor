import { defineBoot } from '#q-app/wrappers';

declare module 'vue' {
  interface ComponentCustomProperties {

    $logUxEvt: Function;
  }
}

const LOJENS_TAG_ID:string = 'UA-58141842-7';
gtag('config',  LOJENS_TAG_ID, {
  'send_page_view': false,
  'groups': 'agency'
});


export default defineBoot(({ app, router, store }) => {


  const logUxEvt =  (evtName$, data$) => {
    // for now Google tag manager
    gtag('event', evtName$, data$);
  };

  router.afterEach((routeTo, routeFrom) => {
    if(routeTo !== undefined){
      logUxEvt('Page-view', {page_path : routeTo.path, page_title: routeTo.meta.title})
    }
  });

  app.config.globalProperties.$logUxEvt = logUxEvt;


});
