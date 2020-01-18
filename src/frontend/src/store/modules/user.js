import Vue from 'vue'
import {
  getToken,
  setToken,
  cleanToken,
  isTokenValid
} from '@/utils/token'

export default {
  state: {
    usersMeta: [],
    user: null,
    token: getToken(),
    departments: [],
    positions: []
  },
  getters: {
    usersMeta (state) {
      return state.usersMeta.map(userMeta => ({
        label: `${userMeta.username} - ${userMeta.email}`,
        value: userMeta.id,
        email: userMeta.email,
        username: userMeta.username
      }))
    },
    role (state) {
      if (state.user) {
        return state.user.authorType > 0 ? '管理员' : '普通用户'
      }
      return ''
    },
    username (state) {
      return state.user ? state.user.username : ''
    },
    headers (state) {
      return {
        Authorization: state.token
      }
    },
    currentUser (state) {
      return state.user
    },
    departments (state) {
      return state.departments
    },
    positions (state) {
      return state.positions
    }
  },
  mutations: {
    updateUsersMeta (state, meta) {
      state.usersMeta = meta
    },
    updateUserProfile (state, user) {
      state.user = user
    },
    cleanUserProfile (state) {
      state.user = null
    },
    refreshUserToken (state, { token, expiredAt }) {
      state.token = setToken(token, expiredAt)
    },
    cleanUserToken (state) {
      state.token = cleanToken()
    },
    updateDepartAndPositions (state, { departments, positions }) {
      state.departments = departments
      state.positions = positions
    }
  },
  actions: {
    async fetchDepartAndPositions ({ commit }) {
      try {
        let res = await Vue.axios.get('system/settings')
        commit('updateDepartAndPositions', { departments: res.departments, positions: res.positions })
      } catch (e) {
      }
    },
    async fetchUsersMeta ({ commit }) {
      let meta = await Vue.axios.get('account/users/meta')
      if (meta.ok) {
        commit('updateUsersMeta', meta.data)
      }
    },
    fetchUserProfile ({ commit }) {
      return !isTokenValid()
        ? Promise.resolve()
        : Vue.axios.get('account/user').then(data => {
          commit('updateUserProfile', data)
        }).catch(() => {})
    },
    async  submitForm ({ commit }, user) {
      let res = await Vue.axios.put('account/user/' + user.id, {
        phone: user.phone,
        username: user.username,
        position: user.position,
        department: user.department,
        avatar: user.avatar
      }).catch(({ status }) => { return false })
      if (res != null) {
        commit('updateUserProfile', user)
        return true
      } else {
        return false
      }
    },
    async submitPasswordChange (context, payload) {
      // let { currentUserId, oldPassword, newPassword, confirmPass } = payload
      let { newPassword } = payload
      try {
        let res = await Vue.axios.put('account/password', {
          newPassword
        })
        return res
      } catch (e) {
      }
    },
    async login ({ commit, dispatch }, params) {
      let data = await Vue.axios.post('account/login', params)
      if (data.ok) {
        commit('refreshUserToken', {
          token: data.token,
          expiredAt: data.expired_at
        })
        await dispatch('fetchUserProfile')
      } else {
        throw new Error(data.msg)
      }
    },
    async logout ({ commit }) {
      await Vue.axios.post('account/logout')
      commit('cleanUserToken')
      commit('cleanUserProfile')
    },
    async awaitLogin ({ getters }) {
      return new Promise(resolve => {
        let timer = setInterval(() => {
          if (getters.currentUser) {
            clearInterval(timer)
            resolve()
          }
        }, 500)
      })
    }
  }
}
