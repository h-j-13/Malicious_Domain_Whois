// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import echarts from "echarts"
import Element from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import './a.js'
Vue.prototype.myURL = "http://172.29.152.3:8000"
Vue.use(Element)

Vue.config.productionTip = false
Vue.use(Vuex)

const store = new Vuex.Store({
	state:{
		index:'/'
	},
})

router.beforeEach((to,from,next) =>{
	if (to.path.indexOf("/sta-info") != -1 )
    {
        store.state.index = '/sta-info/people/people-name'
    }
    else if(to.path.indexOf("/model") != -1 )
    {
        store.state.index = '/model'
    }
    else if (to.path.indexOf("/check") != -1)
    {
        store.state.index = '/check'
    }
    else
    {
        store.state.index = '/'
    }
    //next({path:to});
    //localStorage.head_index = '/sta-info/people/people-name'
    next();
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})