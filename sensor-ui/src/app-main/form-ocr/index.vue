<script setup lang="ts">

</script>

<template>
  <activity-container section-regular  header-class="shadow-1 text-blue-grey-1 bg-deep-purple">
    <template #header>
        <q-toolbar>
          <q-toolbar-title class="text-bold">
            Form OCR
          </q-toolbar-title>
        </q-toolbar>
    </template>
    <template #page>
      <a-page class="bg-grey-1">
        <template #stickyTop>
          <a-section class="bg-deep-purple-10">
            <q-tabs class="text-amber-1 shadow-1" align="left">
              <q-route-tab name="form-upload" label="Upload & Process Form" :to="{name: 'form-ocr.upload'}" />
              <q-route-tab name="form-list" label="Form Library" :to="{name: 'form-ocr.list'}" />
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
