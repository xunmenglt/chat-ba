// src/plugins/vuetify.js

import Vue from 'vue'
import Vuetify from 'vuetify'


Vue.use(Vuetify)

export default new Vuetify({
    icons: {
        iconfont:  'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
    },
    // theme: { dark: true },
});
