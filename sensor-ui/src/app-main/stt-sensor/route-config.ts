import { RouteRecordRaw } from 'vue-router'
import SttIndex from './index.vue'
import IvIndex from './iv-index.vue'

const routes: RouteRecordRaw =
{
  path: '/stt',
  name: 'stt-index',
  component: SttIndex,
  children: [
    {
      path: 'interview',
      name: 'stt-interview',
      component: IvIndex
    }
  ]
}


export default routes
