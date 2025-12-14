import { RouteRecordRaw } from 'vue-router';
import DemoRoute from 'src/app-main/demo-examples/route-config'
import PlayBookRoute from "src/app-main/playbook/route-config"
import IncidentRoute from "src/app-main/incident/route-config"
import FormSensorRoute from 'src/app-main/form-sensor/route-config'
import Index from 'src/app-main/index.vue'


const routes: RouteRecordRaw[] = [
 /* {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
  },*/
  {
    path: '',
    name: 'index',
    component: Index
  },
  {
     ...DemoRoute
  },
  {
    ...PlayBookRoute
  },
  {
    ...IncidentRoute
  },
  {
    ...FormSensorRoute
  },
  {
    path: '/:catchAll(.*)*',
    name: 'catch-all',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
