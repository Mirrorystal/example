export function getHashFullPath () {
  return location.href.split('#')[1] || '/'
}
