import {Ref, ref} from "vue";

 export type DrawerState = {
  drawerVisible : Ref<boolean>,
  showDrawer: Function,
  hideDrawer: Function
}

export default function useDrawerState():DrawerState{
  const drawerVisible = ref(false);
  const showDrawer = ()=>drawerVisible.value = true;
  const hideDrawer = ()=> drawerVisible.value = false;

  return {drawerVisible, showDrawer, hideDrawer}
}

