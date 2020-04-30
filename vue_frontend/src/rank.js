import Vue from 'vue'
import App from './RankApp.vue'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/^ion-/]
Vue.prototype.originalList = window.originalList;
new Vue({
  render: h => h(App),
}).$mount('#rank_app')
