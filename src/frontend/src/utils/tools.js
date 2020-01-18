import Vue from 'vue'

// 判断两个对象所含键值对是否相等,不进行递归比较
export function isObjectValueEqual (a, b) {
  if (a.length !== b.length) return false
  for (let x in a) {
    if (a[x] !== b[x]) { return false }
  }
  return true
}
// 格式化时间
export function formatTime (value) {
  let date = new Date(value)
  let year = date.getFullYear()
  let month = date.getMonth() + 1
  month = month > 9 ? month : ('0' + month)
  let day = date.getDate()
  day = day > 9 ? day : ('0' + day)
  let hh = date.getHours()
  hh = hh > 9 ? hh : ('0' + hh)
  let mm = date.getMinutes()
  mm = mm > 9 ? mm : ('0' + mm)
  let ss = date.getSeconds()
  ss = ss > 9 ? ss : ('0' + ss)
  let time = year + '-' + month + '-' + day + ' ' + hh + ':' + mm + ':' + ss
  return time
}

export function sleep (ms) {
  return new Promise(resolve => {
    setTimeout(resolve, ms)
  })
}

export async function download (url, filename) {
  let data = await Vue.axios.get(url, {
    responseType: 'blob'
  })
  let blob = new Blob([data], { type: data.type })
  let downloadElement = document.createElement('a')
  let href = window.URL.createObjectURL(blob)
  downloadElement.href = href
  downloadElement.download = filename
  document.body.appendChild(downloadElement)
  downloadElement.click()
  document.body.removeChild(downloadElement)
  window.URL.revokeObjectURL(href)
}
