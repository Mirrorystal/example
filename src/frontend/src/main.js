import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import MainLayout from './components/MainLayout'
import './plugins'
import './directives'
import { getHashFullPath } from './utils/url'

Vue.config.productionTip = false
Vue.component('MainLayout', MainLayout)

router.beforeEach(function (to, from, next) {
  store.getters.currentUser === null && to.path !== '/login'
    ? next({
      name: 'login',
      query: { from: getHashFullPath() }
    }) : next()
})

store.dispatch('fetchUserProfile').then(() => {
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app')
})
