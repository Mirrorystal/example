import Vue from 'vue'
import store from '../store'

Vue.directive('role', function (el, binding) {
  let currentUser = store.getters.currentUser
  if (binding.arg === 'admin' && (!currentUser || currentUser.authorType <= 0)) {
    el.style.display = 'none'
  } else {
    el.style.display = ''
  }
})
