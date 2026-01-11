import CVSensorIndex from './index.vue'
import CvUpload from './cv-upload.vue'
import CvList from './cv-list.vue'

import { RouteRecordRaw } from 'vue-router'

const routeConfig: RouteRecordRaw = {
  path: '/cv-sensor',
  name: 'cv-sensor',
  component: CVSensorIndex,
  children:[
    {
      path: '/upload',
      name: 'cv-sensor.upload',
      component: CvUpload,
    },
    {
      path: '/list',
      name: 'cv-sensor.list',
      component: CvList,
    }
  ]
}

export default routeConfig
