<template>
   <q-input
      :autofocus="false"
      :color="focusStyle"
      outlined
      stack-label
      unmasked-value  lazy-rules
      @input="validate"
      :error="calcErrorMsg ? true : undefined"
      :error-message="calcErrorMsg"
      v-bind="$attrs">

        <template v-for="(_, slot) of $scopedSlots" v-slot:[slot]="scope"><slot :name="slot" v-bind="scope"/></template>
</q-input>
</template>

<script>
    import FieldBase from "./field-base.vue";

    export default {
        name: "an-input",
        extends: [FieldBase],


    }
</script>

<style scoped lang="scss">



</style>
