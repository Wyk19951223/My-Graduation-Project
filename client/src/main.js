import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import axios from 'axios'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import App from './App'

import store from './store'

Vue.config.productionTip = false

// 时间转换
Vue.prototype.$parseTime = function (unixTimestamp) {
  function fmtSgl (num) {
    return num >= 10 ? num : '0' + num
  }
  if (unixTimestamp) {
    var date = new Date(unixTimestamp * 1000)
    var formattedTime =
      fmtSgl(date.getHours()) + ':' +
      fmtSgl(date.getMinutes()) + ':' +
      fmtSgl(date.getSeconds())
    return formattedTime
  } else {
    return null
  }
}

Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(ElementUI)
Vue.prototype.$http = axios

// 配置路由
var routes = [
  {
    path: '/',
    redirect: 'monitor'
  },
  {
    path: '/monitor',
    component: require('./components/Monitor').default,
    name: 'monitor'
  },
  {
    path: '/analyser',
    component: require('./components/Analyser').default,
    name: 'analyser'
  }
]
var router = new VueRouter({
  routes: routes
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  store,
  router
})
