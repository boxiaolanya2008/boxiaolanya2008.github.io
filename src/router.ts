import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('./views/HomeView.vue') },
    { path: '/projects', name: 'projects', component: () => import('./views/ProjectsView.vue') },
    { path: '/blog', name: 'blog', component: () => import('./views/BlogView.vue') },
    { path: '/timeline', name: 'timeline', component: () => import('./views/TimelineView.vue') },
  ],
})

export default router
