import { defineBoot } from '#q-app/wrappers';
import axios, { AxiosInstance } from 'axios';

declare module 'vue' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}




const api = axios.create({ baseURL: 'https://api.example.com' });

export default defineBoot(({ app, router, store }) => {

  // making axios accessible from every component (with Options API)
  // i.e., this.$axios and this.$api
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;

});

export { api };
