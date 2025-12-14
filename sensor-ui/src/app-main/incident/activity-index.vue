<script setup lang="ts">
import IncidentInit from './incident-init.vue'

</script>

<template>
  <activity-container   header-class="shadow-1 text-blue-grey-10 bg-white">
    <template #header>
        <q-toolbar  >
          <q-toolbar-title class="text-bold  ">
            Incident Report
          </q-toolbar-title>
        </q-toolbar>
    </template>
    <template #page>
      <a-page class="bg-grey-1">
        <incident-init />
      </a-page>
    </template>
  </activity-container>
</template>

<style scoped>

</style>
