import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import WorkbenchView from '../views/WorkbenchView.vue'
import ServicesView from '../views/ServicesView.vue'
import HistoryView from '../views/HistoryView.vue'
import VoicesView from '../views/VoicesView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  { path: '/', name: 'landing', component: LandingView, meta: { title: '', bare: true } },
  { path: '/workbench', name: 'workbench', component: WorkbenchView, meta: { title: '生成工作台' } },
  { path: '/services', name: 'services', component: ServicesView, meta: { title: '文创服务' } },
  { path: '/history', name: 'history', component: HistoryView, meta: { title: '历史图库' } },
  { path: '/voices', name: 'voices', component: VoicesView, meta: { title: '实践风采' } },
  { path: '/about', name: 'about', component: AboutView, meta: { title: '关于' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.afterEach((to) => {
  document.title = `${to.meta.title ? to.meta.title + ' · ' : ''}河湟皮影 · 智能生成`
})

export default router
