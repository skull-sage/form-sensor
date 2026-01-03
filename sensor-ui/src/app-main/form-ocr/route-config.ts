import FormOcrIndex from './index.vue'
import FormUpload from './form-upload.vue'
import FormList from './form-list.vue'

import { RouteRecordRaw } from 'vue-router'

const routeConfig: RouteRecordRaw = {
  path: '/form-ocr',
  name: 'form-ocr',
  component: FormOcrIndex,
  children:[
    {
      path: 'upload',
      name: 'form-ocr.upload',
      component: FormUpload,
    },
    {
      path: 'list',
      name: 'form-ocr.list',
      component: FormList,
    }
  ]
}

export default routeConfig
