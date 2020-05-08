import Vue from 'vue'
import App from './OccupationApp.vue'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/^ion-/]
Vue.prototype.originalList = window.originalList;
Vue.prototype.error = window.error;
window.rankVue = new Vue({
  render: h => h(App)
}).$mount('#occupation_app')
