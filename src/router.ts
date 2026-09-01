import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn } from './store'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('./views/HomeView.vue') },
    { path: '/blog', name: 'blog', component: () => import('./views/BlogView.vue') },
    { path: '/blog/:slug', name: 'post', component: () => import('./views/PostView.vue') },
    { path: '/projects', name: 'projects', component: () => import('./views/ProjectsView.vue') },
    { path: '/about', name: 'about', component: () => import('./views/AboutView.vue') },
    { path: '/login', name: 'login', component: () => import('./views/LoginView.vue') },
    { path: '/write', name: 'write', component: () => import('./views/WriteView.vue'), meta: { requiresAuth: true } },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

/* 需要登录的路由：未登录跳登录页，登录后回到来源页 */
router.beforeEach((to) => {
  if (to.meta.requiresAuth && !isLoggedIn.value) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})

export default router
