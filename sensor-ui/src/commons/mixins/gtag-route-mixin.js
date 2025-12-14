

export default {
  props: {
    gtagCategory: String,
    gtagLabel: String,
    routeTo: Object|String,
    routeName: String,
    routeParams: Object
  },
  computed:{
    calcRoute(){
      let route;
      if(this.routeTo)
        route = this.routeTo;
      else if(this.routeName){
        route = {name: this.routeName};
        if(this.routeParams)
          route['params'] = this.routeParams;
      }

      return route;
    }

  },
  methods:{
    triggerGtag(name$){

      if(this.gtagCategory && name$){
        this.$gEvent(name$, {
          'event_category': this.gtagCategory,
          'event_label': this.gtagLabel,
        });
      }
    },

    }

}
