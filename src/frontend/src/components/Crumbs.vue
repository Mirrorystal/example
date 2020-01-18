<template>
  <div v-if="!$route.meta.hideCrumbs" class="row wrapper border-bottom white-bg page-heading">
    <div class="col-lg-10">
      <!-- <h2>{{$route.meta.title}}</h2> -->
      <ol class="breadcrumb">
        <li v-for="crumb in crumbs" :key="crumb.path" class="breadcrumb-item" :class="{active: !crumb.path}">
          <strong v-if="!crumb.path">{{crumb.title}}</strong>
          <a v-else :href="formatPath(crumb.path)">{{crumb.title}}</a>
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ads-crumbs',
  props: {
    crumbs: {
      type: Array,
      default () {
        console.log()
        return [{
          title: this.$route.meta.title
        }]
      }
    }
  },
  methods: {
    formatPath (path) {
      path = path.startsWith('/') ? path : '/' + path
      return '#' + path
    }
  }
}
</script>

<style lang="scss" scoped>
.page-heading {
  padding: 20px 10px;
}
</style>
