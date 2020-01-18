<template>
  <div class="row border-bottom">
    <nav class="navbar navbar-static-top white-bg" role="navigation" :style="{marginBottom: 0}">
      <div class="navbar-header">
        <a class="navbar-minimalize minimalize-styl-2 btn btn-primary" @click="toggleNavigation" href="#">
          <i class="fa fa-bars"></i>
        </a>
      </div>
      <ul class="nav navbar-top-links navbar-right">
        <li>
          <a @click="doLogout">
            <i class="fa fa-sign-out"></i>Log out
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { getHashFullPath } from '@/utils/url'
import { smoothlyMenu } from '@/utils/helper'

export default {
  name: 'ads-header',
  methods: {
    ...mapActions(['logout']),
    toggleNavigation (e) {
      e.preventDefault()
      $('body').toggleClass('mini-navbar')
      smoothlyMenu()
    },
    async doLogout () {
      this.logout().then(() => {
        this.$router.push({
          name: 'login',
          query: {
            from: getHashFullPath()
          }
        })
      })
    }
  }
}
</script>
