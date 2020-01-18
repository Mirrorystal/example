import Vue from 'vue'

export default {
  state: {
    systemInfo: {
      departments: [],
      positions: [],
      shieldTypes: [],
      spliceTypes: [],
      interfaceProtocol: []
    }
  },
  // 获取值
  getters: {
    systemInfo: store => store.systemInfo,
    systemDepartments: store => store.systemInfo.departments,
    systemPositions: store => store.systemInfo.positions,
    systemShieldTypes: store => store.systemInfo.shieldTypes,
    systemSpliceTypes: store => store.systemInfo.spliceTypes,
    systemInterfaceProtocol: store => store.systemInfo.interfaceProtocol
  },
  // 赋值
  mutations: {
    updateSystemInfo (state, systemInfo) {
      state.systemInfo = systemInfo
    },
    updateSystemDepartments (state, systemDepartments) {
      state.systemInfo.departments = systemDepartments
    },
    updateSystemPositions (state, systemPositions) {
      state.systemInfo.positions = systemPositions
    },
    updateSystemShieldTypes (state, systemShieldTypes) {
      state.systemInfo.shieldTypes = systemShieldTypes
    },
    updateSystemSpliceTypes (state, systemSpliceTypes) {
      state.systemInfo.spliceTypes = systemSpliceTypes
    },
    updateSystemInterfaceProtocol (state, systemInterfaceProtocol) {
      state.systemInfo.interfaceProtocol = systemInterfaceProtocol
    }
  },
  actions: {
    async fetchSystemInformation ({ commit }) {
      let result = await Vue.axios.get('system/settings')
      commit('updateSystemInfo', result)
    }
  }
}
