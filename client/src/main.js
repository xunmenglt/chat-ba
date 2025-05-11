import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import plugins from './plugins'
// 弹窗工具
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import 'vuetify/dist/vuetify.min.css'
// 引入图标
import '@mdi/font/css/materialdesignicons.css'
// 映入自定义图标
import "@/assets/iconfont/iconfont.css";

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);

Vue.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 3,
  newestOnTop: false
});

Vue.config.productionTip = false

Vue.use(plugins)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
