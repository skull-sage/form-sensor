<template>
  <span>
    <q-icon class="q-mr-xs text-grey-5" :name="icon" v-if="icon"/>
    <span>{{calcDaTime}}</span>
    <q-tooltip>
      {{daTime}}
    </q-tooltip>
  </span>
</template>

<script>

import {fAgoFromNow, fDateTime} from 'src/commons/utils/lang-util'

export default {
  name: "a-date-time",
  props: {
    utc: String,
    icon: {
      type: String,
      default: 'r_access_time'
    },
    langCode: {
      type: String,
      default: 'en'
    }
  },

  computed:{
    daTime(){
      if(this.utc == undefined) return undefined;
      return fDateTime(this.utc, this.langCode);
    },
    calcDaTime(){
      if(this.utc == undefined) return undefined;
      return fAgoFromNow(this.utc, this.langCode)
    }
  }

}
</script>

<style scoped>

</style>
