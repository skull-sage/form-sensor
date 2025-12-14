<script   lang="ts">
import {defineComponent} from "vue";

export default defineComponent({

  async mounted() {
    await this.loadCats();
  },
  data(){
    return {
      loading: false
    }
  },
  methods:{
    async loadCats(){
      this.loading = true;
      let {data} = await this.$axios.get("http://localhost:3000/cats");
      this.cats = data;
      this.loading = false;
      console.log(this.cats);
    },
    async createNew(){
      let data = await this.$axios.post("http://localhost:3000/cats/create", {name: 'mina', age: 7, breed: 'mixed'});
      this.cats = data;
      console.log(this.cats);
    },
    getById(){

    }
  }

})

</script>

<template>
  <div class="q-pa-lg">
    <q-list class="bg-grey-1">
      <q-spinner v-if="loading" />
      <template  v-else >
        <q-item-label caption v-if="this.cats">We Have {{this.cats.length}}  Cats</q-item-label>
        <q-item v-for="cat in this.cats">
          <q-item-section>
            <q-item-label title>{{cat.name}}</q-item-label>
            <q-item-label>he is {{cat.age}} years old and he is {{cat.breed}} breed</q-item-label>
          </q-item-section>
        </q-item>
      </template>
    </q-list>
    <a-btn action primary label="Create new" @click="createNew" />
  </div>
</template>

<style scoped>

</style>
