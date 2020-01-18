export default {
  state: {
    equipmentTemplates: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    deviceTemplates: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    interfaceTemplates: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    },
    cableTemplates: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    }
  },

  getters: {
    equipmentTemplatesPagination: state => state.equipmentTemplates.pagination,
    deviceTemplatesPagination: state => state.deviceTemplates.pagination,
    interfaceTemplatesPagination: state => state.interfaceTemplates.pagination,
    cableTemplatesPagination: state => state.cableTemplates.pagination,
    equipmentTemplatesTotalCount: state => state.equipmentTemplates.pagination.totalCount,
    deviceTemplatesTotalCount: state => state.deviceTemplates.pagination.totalCount,
    interfaceTemplatesTotalCount: state => state.interfaceTemplates.pagination.totalCount,
    cableTemplatesTotalCount: state => state.cableTemplates.pagination.totalCount
  },
  mutations: {
    updateEquipmentTemplatePagination (state, pagination) {
      state.equipmentTemplates.pagination = pagination
    },
    updateDeviceTemplatePagination (state, pagination) {
      state.deviceTemplates.pagination = pagination
    },
    updateInterfaceTemplatePagination (state, pagination) {
      state.interfaceTemplates.pagination = pagination
    },
    updateCableTemplatePagination (state, pagination) {
      state.cableTemplates.pagination = pagination
    }
  },
  actions: {}
}
