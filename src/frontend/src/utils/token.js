import Vue from 'vue'
const STORAGE_TOKEN_KEY = '_api_token'
const STORAGE_TOKEN_EXPIRED_KEY = '_api_token_expired_at'
const TOKEN_PREFIX = 'Bearer '

export function getToken () {
  let token = localStorage.getItem(STORAGE_TOKEN_KEY)
  return token
    ? TOKEN_PREFIX + token
    : ''
}

export function setToken (token, expiredTime) {
  localStorage.setItem(STORAGE_TOKEN_KEY, token)
  localStorage.setItem(STORAGE_TOKEN_EXPIRED_KEY, new Date().getTime() + expiredTime * 1000)
  token = getToken()
  Vue.axios.refreshToken(token)
  return token
}

export function cleanToken () {
  localStorage.setItem(STORAGE_TOKEN_KEY, '')
  localStorage.setItem(STORAGE_TOKEN_EXPIRED_KEY, new Date().getTime())
  Vue.axios.refreshToken()
}

export function isTokenValid () {
  let expiredAt = localStorage.getItem(STORAGE_TOKEN_EXPIRED_KEY)
  return expiredAt
    ? Number(expiredAt) > new Date().getTime()
    : false
}
