<script setup lang="ts">

import DemoPage from "./demo-page.vue";
</script>

<template>
  <activity-container  section-normal
                       header-class="shadow-1 bg-white text-blue-grey-10">
    <template #header>
        <q-toolbar  class="q-px-none">
          <btn-drawer-open />
          <q-toolbar-title>
            Demo Activity
          </q-toolbar-title>
          <q-btn flat round dense icon="r_apps" class="q-mr-xs" />
        </q-toolbar>
    </template>
    <template #page>
      <demo-page />
    </template>
    <template #drawerMenu>
      <a-drawer />
    </template>
  </activity-container>
</template>

<style scoped>

</style>
