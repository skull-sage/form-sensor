<script setup lang="ts">

</script>

<template>
  <activity-container section-regular  header-class="shadow-1 text-blue-grey-1 bg-indigo">
    <template #header>
        <q-toolbar>
          <q-toolbar-title class="text-bold">
            CV Analysis
          </q-toolbar-title>
        </q-toolbar>
    </template>
    <template #page>
      <a-page class="bg-grey-1">
        <template #stickyTop>
          <a-section class="bg-indigo-10">
            <q-tabs class="text-amber-1 shadow-1" align="left">
              <q-route-tab name="cv-upload" label="Upload & Analyze CV" :to="{name: 'doc-sensor.upload'}" />
              <q-route-tab name="cv-list" label="CV Library" :to="{name: 'doc-sensor.list'}" />
            </q-tabs>
          </a-section>
        </template>
        <template #default>
          <router-view></router-view>
        </template>
      </a-page>
    </template>
  </activity-container>
</template>

<style scoped>

</style>
