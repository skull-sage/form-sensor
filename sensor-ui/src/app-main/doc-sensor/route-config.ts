import DocSensorIndex from './index.vue'
import CvUpload from './cv-upload.vue'
import CvList from './cv-list.vue'

import { RouteRecordRaw } from 'vue-router'

const routeConfig: RouteRecordRaw = {
  path: '/doc-sensor',
  name: 'doc-sensor',
  component: DocSensorIndex,
  children:[
    {
      path: '/upload',
      name: 'doc-sensor.upload',
      component: CvUpload,
    },
    {
      path: '/list',
      name: 'doc-sensor.list',
      component: CvList,
    }
  ]
}

export default routeConfig
