import Vue from 'vue'
import { ValidationProvider, extend } from 'vee-validate'
import { required, email } from 'vee-validate/dist/rules'

extend('required', {
  ...required,
  message: '{_field_}不能为空'
})

extend('email', {
  ...email,
  message: '请输入正确的{_field_}'
})

Vue.component('ValidationProvider', ValidationProvider)
