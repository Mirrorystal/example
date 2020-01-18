import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export default new VueRouter({
  mode: 'hash',
  routes: [{
    path: '/',
    redirect: '/main'
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../pages/Login.vue')
  }, {
    path: '/main',
    name: 'main',
    meta: {
      title: '主页'
    },
    component: () => import(/* webpackChunkName: "appliance" */ '../pages/main/Main.vue')
  }, {
    path: '/minor',
    name: 'minor',
    meta: {
      title: '副页'
    },
    component: () => import(/* webpackChunkName: "template" */ '../pages/minor/Minor.vue')
  }
  ]
})
