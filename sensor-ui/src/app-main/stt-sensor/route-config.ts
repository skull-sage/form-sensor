import { RouteRecordRaw } from 'vue-router'
import SttIndex from './index.vue'

const routes: RouteRecordRaw =
  {
    path: '/stt',
    name: 'stt',
    children: [
      {
        path: '',
        name: 'stt-index',
        component: SttIndex
      }
    ]
  }


export default routes
