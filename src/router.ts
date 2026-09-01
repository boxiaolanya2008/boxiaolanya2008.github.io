import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: () => import('./views/HomeView.vue') },
    { path: '/blog', name: 'blog', component: () => import('./views/BlogView.vue') },
    { path: '/blog/:slug', name: 'post', component: () => import('./views/PostView.vue') },
    { path: '/projects', name: 'projects', component: () => import('./views/ProjectsView.vue') },
    { path: '/about', name: 'about', component: () => import('./views/AboutView.vue') },
  ],
})

export default router
