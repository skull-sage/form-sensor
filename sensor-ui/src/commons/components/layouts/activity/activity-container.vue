<template>
  <q-layout view="hHh LpR fFf" :class="[sectionStyle]">
    <q-header :reveal="headerReveal"
              class="a-section"
              :class="[headerClass]"
    >
        <slot name="header"></slot>
    </q-header>
    <q-drawer v-if="$slots.drawerMenu"
      @show="$emit('menu-opened')" @hide="hideDrawer()" :model-value="drawerVisible"
      bordered behavior="mobile" :width="340" :breakpoint="700">
        <slot name="drawerMenu" v-if="drawerVisible"></slot>
    </q-drawer>
    <q-page-container class="bg-white overflow-hidden-x">
      <slot name="page"></slot>
    </q-page-container>
    <q-footer :reveal="footerReveal"
              class="transparent shadow-0">
        <slot name="footer"></slot>
    </q-footer>
  </q-layout>
</template>

<script setup lang="ts">
  import  useDrawerState from "./use-drawer-state.js";
  import type {DrawerState} from "./use-drawer-state.js";
  import {provide, computed, ref} from "vue"

  const props = defineProps({
    headerReveal: { type: Boolean, default: true},
    footerReveal: {type: Boolean, default: true},
    drawerBehavior: {type: String, default: "mobile"},
    headerClass: {type: String},
    footerClass: {type:String},
    // drawerName: String,
    // containerState affect standard space in x-direction of b-container/section-container
    // containerState :: {std, extended, small}

    sectionRegular: {type: Boolean, default: true},
    sectionExpanded: {type: Boolean, default: false},
    sectionSmall: {type: Boolean, default: false}

  });

  const  sectionStyle = computed(()=> {
    if(props.sectionExpanded)
      return "section-expanded" // no-modifier is expanded
    else if(props.sectionSmall)
      return "section-small" // class .small modifier
    else
      return "section-regular"// class .normal modifier
  });



  const {drawerVisible, showDrawer, hideDrawer}:DrawerState = useDrawerState();
  provide('drawer_state', {drawerVisible, showDrawer, hideDrawer})


</script>
<style lang="scss">

  .q-layout .a-section{
    padding-left: 16px;
    padding-right: 16px;
  }

  .q-layout.section-regular  .a-section {

    @media (min-width : $breakpoint-lg-min){
      padding-left:12%;
      padding-right: 12%;
    }

    @media (min-width : $breakpoint-sm-min) and (max-width : $breakpoint-md-max){
      padding-left:4%;
      padding-right: 4%;
    }

  }

  .q-layout.section-small  .a-section
  {
    @media (min-width : $breakpoint-lg-min){
      padding-left:24%;
      padding-right: 24%;
    }
    @media (min-width : $breakpoint-sm-min) and (max-width : $breakpoint-md-max){
      padding-left:8%;
      padding-right: 8%;
    }
  }

  .q-layout .q-toolbar {
    padding-left: 0;
    padding-right: 0;
  }

</style>
