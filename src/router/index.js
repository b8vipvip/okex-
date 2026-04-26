import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

const routes = [
  { path: '/login', component: () => import('../views/LoginView.vue') },
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      { path: '/dashboard', component: () => import('../views/DashboardView.vue') },
      { path: '/import', component: () => import('../views/ImportView.vue') },
      { path: '/tasks', component: () => import('../views/TasksView.vue') },
      { path: '/tasks/:id', component: () => import('../views/TaskDetailView.vue') },
      { path: '/batches', component: () => import('../views/BatchesView.vue') }
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('admin_token')
  if (to.path !== '/login' && !token) return next('/login')
  if (to.path === '/login' && token) return next('/dashboard')
  next()
})

export default router
