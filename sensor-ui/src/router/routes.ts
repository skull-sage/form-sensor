import { RouteRecordRaw } from 'vue-router';
import DemoRoute from 'src/app-main/demo-examples/route-config'
import FormSensorRoute from 'src/app-main/form-sensor/route-config'
import DocSensorRoute from 'src/app-main/doc-sensor/route-config'
import STTSensorRoute from 'src/app-main/stt-sensor/route-config'
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
    ...FormSensorRoute
  },
  {
    ...DocSensorRoute
  },
  {
    ...STTSensorRoute
  },
  {
    path: '/:catchAll(.*)*',
    name: 'catch-all',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
