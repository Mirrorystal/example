<template>
  <div id="wrapper">
    <ads-nav :path="$route.path"></ads-nav>
    <div id="page-wrapper" class="gray-bg">
      <ads-header></ads-header>
      <ads-crumbs :crumbs="crumbs"></ads-crumbs>
      <div class="wrapper wrapper-content animated fadeIn">
        <slot></slot>
      </div>
      <ads-footer></ads-footer>
    </div>
  </div>
</template>

<script>
import AdsNav from './Navigation'
import AdsCrumbs from './Crumbs'
import AdsFooter from './Footer'
import AdsHeader from './Header'
import pace from '../libs/pace'
import { correctHeight, detectBody } from '../utils/helper'

export default {
  name: 'main-layout',
  props: ['crumbs'],
  components: {
    AdsNav, AdsCrumbs, AdsHeader, AdsFooter
  },
  mounted () {
    pace.start()
    $(window).bind('load resize', () => {
      correctHeight()
      detectBody()
    })

    $('.metismenu a').click(() => {
      setTimeout(() => {
        correctHeight()
      }, 300)
    })
  }
}
</script>
