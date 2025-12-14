<script setup lang="ts">

</script>

<template>
  <activity-container section-regular  header-class="shadow-1 text-blue-grey-1 bg-teal">
    <template #header>
        <q-toolbar>
          <q-toolbar-title class="text-bold  ">
            Smart Form
          </q-toolbar-title>
        </q-toolbar>
    </template>
    <template #page>
      <a-page class="bg-grey-1">
        <template #stickyTop>
          <a-section class="bg-teal-10 ">
            <q-tabs class="text-amber-1 shadow-1" align="left"  >
              <q-route-tab name="sensor-crud" label="Manage Smart Fields" :to="{name: 'smart-form.crud'}" />
              <q-route-tab name="sensor-check" label="Test Field" :to="{name: 'smart-form.verify'}" />
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
