<template>
  <q-breadcrumbs :active-color="activeColor">
    <template v-slot:separator>
      <q-icon
        size="1.5rem"
        name="chevron_right"
        :color=separtorColor
      />
    </template>
    <q-breadcrumbs-el v-for="(crumb, index) in crumbList"
                      :key = "index"
                      :label="crumb.label"
                      :to="crumb.route" />
    <!--<q-breadcrumbs-el label="COURSE" />-->
  </q-breadcrumbs>
</template>

<script>
    export default {
        name: "a-bread-crumbs",
        props: {
          crumbList : Array, // crumb :: Object -> {label :: string, route :: Object -> {name:: string, params: Object}}
          activeColor: {
            type :  String,
            default : 'blue-grey-8',
          },
          separtorColor:{
            type :  String,
            default : 'primary',
          }
        }

    }
</script>

<style scoped>

</style>
