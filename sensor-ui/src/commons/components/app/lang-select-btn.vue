<template>
  <q-btn-toggle
    unelevated
    :value="langCode"
    @input="changeLangCode"
    toggle-color="blue-grey-7"
    color="blue-grey-1"
    text-color="blue-grey-7"
    :options="[
                  {label: 'EN', value: 'en'},
                  {label: 'BN', value: 'bn'}
                ]"
  />
</template>

<script>
import {Cookies} from 'quasar'

    export default {
        name: "lang-select-btn",

        methods:{
          changeLangCode(val$)
          {
            Cookies.set('lang-code', val$, {expires: 365});
            window.location.reload();
          }
        }

    }
</script>

<style scoped>

</style>
