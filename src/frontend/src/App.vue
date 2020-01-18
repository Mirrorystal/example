<template>
  <div id="app">
    <router-view/>
    <progress-manager ref="progressManager"></progress-manager>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapActions } from 'vuex'
import ProgressManager from '@/components/ProgressManager.vue'

export default {
  name: 'app',
  components: { ProgressManager },
  mounted () {
    Vue.prototype.$progress = this.$refs.progressManager
    this.awaitLogin().then(() => {
      this.$store.dispatch('fetchUsersMeta')
      this.$store.dispatch('fetchSystemInformation')
      this.$store.dispatch('fetchEquipmentMeta')
      this.$store.dispatch('fetchDeviceMeta')
      this.$store.dispatch('fetchInterfaceMeta')
    })
    this.eventHub.$on('change:user', () => {
      this.$store.dispatch('fetchUsersMeta')
    })
    this.eventHub.$on('change:setting', () => {
      this.$store.dispatch('fetchSystemInformation')
    })
    this.eventHub.$on('change:equipment', () => {
      this.$store.dispatch('fetchEquipmentMeta')
    })
    this.eventHub.$on('change:device', () => {
      this.$store.dispatch('fetchDeviceMeta')
    })
    this.eventHub.$on('change:interface', () => {
      this.$store.dispatch('fetchInterfaceMeta')
    })
  },
  methods: {
    ...mapActions(['awaitLogin'])
  }
}
</script>

<style lang="scss">
.full-width {
  width: 100%;
}
</style>
