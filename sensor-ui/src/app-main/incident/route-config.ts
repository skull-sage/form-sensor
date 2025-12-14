import {RouteRecordRaw} from "vue-router";
import IncidentIndex from "./activity-index.vue"
import IncidentList from "./incident-list/index.vue";
import IncidentDetails from "./an-incident/incident-details.vue";

const routeConfig: RouteRecordRaw =  {
  path: '/incident',
  name: 'incident',
  component: IncidentIndex,
  // children: [
  //   {path: '', redirect: {name: 'incident-list'}},
  //   {
  //     path: 'list',
  //     name: 'incident-list',
  //     component: IncidentList
  //   },
  //   {
  //     path: 'details/:id',
  //     name: 'incident-detail',
  //     component: IncidentDetails,
  //   }
  // ]

}

export default routeConfig;
