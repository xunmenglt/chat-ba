import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path:'/dashboard',
    name:'dashboard',
    component:DashboardView,
    redirect:"/dashboard/knowledgebase",
    children:[
      {
        path:'/dashboard/chat',
        name:'chat',
        component: () => import('../views/chat/chat.vue'),
      },
      {
        path:'/dashboard/retrieval',
        name:'retrieval',
        component: () => import('../views/retrieval/retrieval.vue'),
      },
      {
        path:"/dashboard/generation",
        name:'generation',
        component: () => import('../views/generation/index.vue'),
      },
      {
        path:"/dashboard/model_pk",
        name:"model_pk",
        component: () => import('../views/model_pk/index.vue'),
      },
      {
        path:'/dashboard/report_extraction',
        name:"report_extraction",
        component: () => import('../views/report_extraction/index.vue'),
      },
      {
        path:'/dashboard/knowledgebase',
        name:'knowledgebase',
        component: () => import('../views/knowledgebase/knowledgebase.vue'),
      },
      {
        path:'/dashboard/knowledgebase/filemanage',
        name:'filemanage',
        component: () => import('../views/knowledgebase/filemanage/filemanage.vue'),
      },

    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
