<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  props: {
    gtagCategory: { type: String },
    gtagLabel: { type: String },
    routeTo: { type: [Object, String] as PropType<Record<string, any> | string> }, // just like route to
    routeName: { type: String },
    routeParams: { type: Object as PropType<Record<string, any>> }
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
    triggerGtag(name){

      if(this.gtagCategory && name){
        this.$logUxEvt(name, {
          'event_category': this.gtagCategory,
          'event_label': this.gtagLabel
        });
      }

    }

  }
})
</script>

