export default {
  state: {
    equipmentOfRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    deviceOfRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    interfaceOfRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    cableOfRecycle: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    }
  },

  getters: {
    equipmentOfRecyclePagination: state => state.equipmentOfRecycle.pagination,
    deviceOfRecyclePagination: state => state.deviceOfRecycle.pagination,
    interfaceOfRecyclePagination: state => state.interfaceOfRecycle.pagination,
    cableOfRecyclePagination: state => state.cableOfRecycle.pagination,
    equipmentOfRecycleTotalCount: state => state.equipmentOfRecycle.pagination.totalCount,
    deviceOfRecycleTotalCount: state => state.deviceOfRecycle.pagination.totalCount,
    interfaceOfRecycleTotalCount: state => state.interfaceOfRecycle.pagination.totalCount,
    cableOfRecycleTotalCount: state => state.cableOfRecycle.pagination.totalCount
  },
  mutations: {
    updateOfEquipmentRecyclePagination (state, pagination) {
      state.equipmentOfRecycle.pagination = pagination
    },
    updateOfDeviceRecyclePagination (state, pagination) {
      state.deviceOfRecycle.pagination = pagination
    },
    updateOfInterfaceRecyclePagination (state, pagination) {
      state.interfaceOfRecycle.pagination = pagination
    },
    updateOfCableRecyclePagination (state, pagination) {
      state.cableOfRecycle.pagination = pagination
    }
  },
  actions: {}
}
