<script setup lang="ts">

</script>

<template>
  <activity-container   header-class="text-blue-grey-10 bg-white">
    <template #header>
        <q-toolbar  >
          <btn-drawer-open />
          <q-toolbar-title class="text-bold  ">
            PlayBook
          </q-toolbar-title>
          <q-btn flat round dense icon="r_apps" class="q-mr-xs" />
        </q-toolbar>
    </template>
    <template #page>
      <router-view></router-view>
    </template>
    <template #drawerMenu>
      <a-drawer />
    </template>
  </activity-container>
</template>

<style scoped>

</style>
