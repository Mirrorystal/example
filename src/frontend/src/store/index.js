import Vue from 'vue'
import Vuex from 'vuex'
import userStore from './modules/user'
import applianceStore from './modules/appliance'
import templateStore from './modules/template'
import templateRecycleStore from './modules/templateRecycle'
import applianceRecycleStore from './modules/applianceRecycle'
import systemStore from './modules/system'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    userStore,
    applianceStore,
    templateStore,
    templateRecycleStore,
    applianceRecycleStore,
    systemStore
  }
})
