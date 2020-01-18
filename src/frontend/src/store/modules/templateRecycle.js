export default {
  state: {
    equipmentRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    deviceRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    interfaceRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    cableRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    }
  },

  getters: {
    equipmentRecyclePagination: state => state.equipmentRecycle.pagination,
    deviceRecyclePagination: state => state.deviceRecycle.pagination,
    interfaceRecyclePagination: state => state.interfaceRecycle.pagination,
    cableRecyclePagination: state => state.cableRecycle.pagination,
    equipmentRecycleTotalCount: state => state.equipmentRecycle.pagination.totalCount,
    deviceRecycleTotalCount: state => state.deviceRecycle.pagination.totalCount,
    interfaceRecycleTotalCount: state => state.interfaceRecycle.pagination.totalCount,
    cableRecycleTotalCount: state => state.cableRecycle.pagination.totalCount
  },
  mutations: {
    updateEquipmentRecyclePagination (state, pagination) {
      state.equipmentRecycle.pagination = pagination
    },
    updateDeviceRecyclePagination (state, pagination) {
      state.deviceRecycle.pagination = pagination
    },
    updateInterfaceRecyclePagination (state, pagination) {
      state.interfaceRecycle.pagination = pagination
    },
    updateCableRecyclePagination (state, pagination) {
      state.cableRecycle.pagination = pagination
    }
  },
  actions: {}
}
