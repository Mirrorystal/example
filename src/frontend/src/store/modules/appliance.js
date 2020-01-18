import Vue from 'vue'

export default {
  state: {
    equipment: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      },
      meta: []
    },
    device: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      },
      meta: []
    },
    interface: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      },
      meta: []
    },
    cable: {
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      }
    }
  },
  getters: {
    applianceMeta: state => ({
      equipment: state.equipment.meta,
      device: state.device.meta,
      interface: state.interface.meta
    }),
    equipmentMeta: state => {
      return state.equipment.meta.map(equipment => ({
        value: equipment.id,
        label: equipment.name
      }))
    },
    equipmentPagination: state => state.equipment.pagination,
    equipmentTotalCount: state => state.equipment.pagination.totalCount,
    deviceMeta: state => {
      let equipmentIds = new Set()
      state.device.meta.forEach(device => {
        equipmentIds.add(device.parentEquipmentId)
      })
      return state.equipment.meta.filter(equipment => {
        return equipmentIds.has(equipment.id)
      }).map(equipment => ({
        value: equipment.id,
        label: equipment.name,
        children: state.device.meta.filter(device => {
          return equipment.id === device.parentEquipmentId
        }).map(device => ({
          value: device.id,
          label: device.name
        }))
      }))
    },
    devicePagination: state => state.device.pagination,
    deviceTotalCount: state => state.device.pagination.totalCount,
    interfaceMeta: state => {
      let deviceIds = new Set()
      state.interface.meta.forEach(_interface => {
        deviceIds.add(_interface.parentDeviceId)
      })
      let devicesMeta = state.device.meta.filter(device => {
        return deviceIds.has(device.id)
      }).map(device => ({
        value: device.id,
        label: device.name,
        parentEquipmentId: device.parentEquipmentId,
        children: state.interface.meta.filter(_interface => {
          return _interface.parentDeviceId === device.id
        }).map(_interface => ({
          value: _interface.id,
          label: _interface.name
        }))
      }))

      let equipmentIds = new Set()
      devicesMeta.forEach(device => {
        equipmentIds.add(device.parentEquipmentId)
      })
      return state.equipment.meta.filter(equipment => {
        return equipmentIds.has(equipment.id)
      }).map(equipment => ({
        value: equipment.id,
        label: equipment.name,
        children: devicesMeta.filter(device => {
          return equipment.id === device.parentEquipmentId
        })
      }))
    },
    interfacePagination: state => state.interface.pagination,
    interfaceTotalCount: state => state.interface.pagination.totalCount,
    cablePagination: state => state.cable.pagination,
    cableTotalCount: state => state.cable.pagination.totalCount
  },
  mutations: {
    updateEquipmentPagination (state, pagination) {
      state.equipment.pagination = pagination
    },
    updateEquipmentMeta (state, meta) {
      state.equipment.meta = meta
    },
    updateDevicePagination (state, pagination) {
      state.device.pagination = pagination
    },
    updateDeviceMeta (state, meta) {
      state.device.meta = meta
    },
    updateInterfacePagination (state, pagination) {
      state.interface.pagination = pagination
    },
    updateInterfaceMeta (state, meta) {
      state.interface.meta = meta
    },
    updateCablePagination (state, pagination) {
      state.cable.pagination = pagination
    }
  },
  actions: {
    fetchEquipmentMeta ({ commit }) {
      return Vue.axios.get('appliance/equipments/meta').then(({ data }) => {
        commit('updateEquipmentMeta', data || [])
      })
    },
    fetchDeviceMeta ({ commit }) {
      return Vue.axios.get('appliance/devices/meta').then(({ data }) => {
        commit('updateDeviceMeta', data || [])
      })
    },
    fetchInterfaceMeta ({ commit }) {
      return Vue.axios.get('appliance/interfaces/meta').then(({ data }) => {
        commit('updateInterfaceMeta', data || [])
      })
    }
  }
}
