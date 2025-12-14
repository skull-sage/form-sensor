<template>
  <div class="">
    <!-- learning id checking for anonymous learning needs to be worked on-->
    <!--<q-btn flat  v-if="isRegUser"
           @click="toggleUserMenu()"
           v-bind:class="menuBtnClz"
           class="menu-btn q-px-sm full-height"
    >
      <q-avatar color="violet-10" text-color="white" size="lg">{{loggedUser.cap_letter}}</q-avatar>
    </q-btn>-->
    <q-btn flat v-if="isRegUser == false" to="/auth/sign-in" color="blue-grey-8" label="SIGN IN" class="menu-btn q-px-sm full-height"></q-btn>
  </div>

</template>

<script>
  //import {atobUTF8} from "../boot/Base64";
  import {mapState, mapMutations} from 'vuex';
 // import GraphemeSplitter from 'grapheme-splitter'

  //const gphSplitter = new GraphemeSplitter();


  export default {
        name: "logged-user",
        data(){
          return {
            user_status: ['reg_user', 'r_anonymous', 'g_anonymous']
          }
        },
        computed:
        {
          ...mapState(['loggedUser']),
          menuBtnClz()
          {
            return {'bg-blue-grey-1 text-white' : this.userMenuOpened};

          },

          isRegUser(){
            return this.loggedUser.status === 'reg_user'
          }


        },
        methods:
          {
              ...mapMutations(['toggleUserMenu'])
          }
    }
</script>

<style scoped>
  .menu-btn
  {
    border-radius: 0;
  }
</style>
