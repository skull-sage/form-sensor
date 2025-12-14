import PocIndex from './index.vue'
import FieldList from './field-list.vue'
import FieldVerify from './field-verify.vue'

import { RouteRecordRaw } from 'vue-router'

const routeConfig: RouteRecordRaw = {
  path: '/smart-form',
  name: 'smart-form',
  component: PocIndex,
  children:[
    {
      path: '/list',
      name: 'smart-form.crud',
      component: FieldList,
    },
    {
      path: '/verify',
      name: 'smart-form.verify',
      component: FieldVerify,
    }
  ]
}

export default routeConfig
