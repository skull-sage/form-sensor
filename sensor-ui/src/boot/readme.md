
### Boot file

```ts

const api = axios.create({ baseURL: 'https://api.example.com' });

export default defineBoot(({ app, router, store }) => {
  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

```
Be careful when using SSR for cross-request state pollution
due to creating a Singleton instance here;
If any client changes this (global) instance, it might be a
good idea to move this instance creation inside of the
`export default defineBoot(({app, router, store}) => { /*code*/})`
function in boot (which runs individually
for each client)
