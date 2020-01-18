import qs from 'qs'
import Vue from 'vue'
import axios from 'axios'
import router from '../router'
import { getToken } from '../utils/token'
import { getHashFullPath } from '../utils/url'

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
let messageLock = false

let config = {
  baseURL: '/api',
  timeout: 60 * 1000,
  withCredentials: true,
  headers: {
    Authorization: getToken()
  }
}

const _axios = axios.create(config)
_axios.interceptors.request.use(
  function (config) {
    config.paramsSerializer = params => qs.stringify(params)
    config.data = qs.stringify(config.data)
    return config
  },
  function (error) {
    return Promise.reject(error)
  }
)

_axios.interceptors.response.use(
  function ({ data }) {
    return data
  },
  function ({ response }) {
    switch (response.status) {
      case 401:
        if (getToken() && !messageLock) {
          messageLock = true
          setTimeout(() => {
            messageLock = false
          }, 500)
          Vue.prototype.$message({ message: '登陆已失效', type: 'warning' })
        }
        router.push({ name: 'login', query: { from: getHashFullPath() } })
        break
      case 403:
        Vue.prototype.$message({ message: '权限不足', type: 'warning' })
        break
    }
    return Promise.reject(response)
  }
)

_axios.refreshToken = function (token) {
  this.defaults.headers['Authorization'] = token
}

Plugin.install = function (Vue) {
  Vue.axios = _axios
  Object.defineProperty(Vue.prototype, '$axios', {
    get: () => _axios
  })
}

Vue.use(Plugin)
