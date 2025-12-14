<script setup lang="ts">
import {useRouter} from 'vue-router'
import {ref} from "vue";

const router = useRouter();
const routeList = router.options.routes;
const selectedRoute = ref(routeList[1])

</script>

<template>
  <div class="full-width q-pa-xl ">
    <h1 class="text-h4 text-weight-medium">PlayBook Route List</h1>
    <div class="row q-gutter-lg">
      <div class="col-md-4">
        <div class="q-mb-md">
          Each applications are organized according to a root route.
          We will use named-route, hierarchy is established with dot(.) separation.
          As an example, for an application <b>zerometry</b>
          Routes could be [<i>zerometry</i>, <i>zerometry.todo-list</i>]
        </div>
        <q-list bordered separator round>
          <a-nav-item v-for="aRoute in routeList"
                  :key="aRoute.name"
                  @click="selectedRoute = aRoute"
          >
            <q-item-section >
              <q-item-label :class="{'text-indigo': aRoute.name === selectedRoute.name}">
                {{aRoute.name}}
              </q-item-label>
              <q-item-label  caption v-if="aRoute.children && aRoute.children.length">
                {{aRoute.children?.length}} routes
              </q-item-label>
            </q-item-section>
          </a-nav-item>
        </q-list>
      </div>
      <div class="col-md-4">
        <q-list class="bg-blue-1 q-pa-md" separator>
          <div class="text-h6 text-bold q-mb-sm">{{selectedRoute.name}}</div>
          <a-nav-item v-for="item in selectedRoute.children"
                   :key="item.name"
                   :route-name="item.name"
          >
            <q-item-section>
              <q-item-label>{{item.name}}</q-item-label>
              <q-item-label caption> {{selectedRoute.path}}/{{item.path}}</q-item-label>
            </q-item-section>
          </a-nav-item>
        </q-list>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
