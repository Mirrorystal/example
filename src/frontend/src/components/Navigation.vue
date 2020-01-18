<template>
  <nav class="navbar-default navbar-static-side" role="navigation">
    <ul class="nav metismenu" id="side-menu" ref="menu">
      <li class="nav-header">
        <div class="dropdown profile-element">
          <span class="clear">
            <span class="block m-t-xs">
              <strong class="font-bold username">{{username}}</strong>
            </span>
            <span class="text-muted small block">{{role}}</span>
          </span>
        </div>
      </li>
      <li :class="navActive('/main')">
        <router-link to="/main">
          <i class="el-icon-s-cooperation"></i>
          <span class="nav-label">主页</span>
        </router-link>
      </li>
      <li :class="navActive('/minor')">
        <router-link to="/minor">
          <i class="el-icon-s-order"></i>
          <span class="nav-label">副页</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: ['path'],
  mounted () {
    const { menu } = this.$refs
    $(menu).metisMenu()
  },
  computed: {
    ...mapGetters(['username', 'role'])
  },
  methods: {
    navActive (path) {
      return this.path === path ? 'active' : ''
    }
  }
}
</script>

<style scoped>
.dropdown span {
  color: #DFE4ED;
}

.username {
  letter-spacing: 2px;
}
</style>
