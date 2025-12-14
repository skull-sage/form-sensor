<template>
  <q-field
    :autofocus="false"
    class="an-input "
    :color="focusStyle"
    outlined
    stack-label
    lazy-rules
    :error="calcErrorMsg"
    :error-message="calcErrorMsg"
    v-bind="$attrs">

    <template v-for="(_, slot) in $slots" v-slot:[slot]="scope">
      <slot :name="slot" v-bind="scope || {}" />
    </template>

  </q-field>
</template>

<script>
  import FieldBase from './field-base.vue'

    export default {
        name: "a-field",
        extends: FieldBase,
    }
</script>

<style scoped>

</style>
