import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
    {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
    },
    {
    path: '/menus',
    name: 'Menus',
    component: () => import('../views/Menu.vue')
    },
    {
    path: '/menu/:id',
    name: 'MenuDetail',
    component: () => import('../views/MenuDetail.vue')
    },
    {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue')
    },
    {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
    },
    {
    path: '/register',
    name: 'Register',
    component: () => import('../views/inscription.vue')
    },
    {
    path: '/commande',
    name: 'Commande',
    component: () => import('../views/Commande.vue')
    },
    {
    path: '/mes-commandes',
    name: 'MesCommandes',
    component: () => import('../views/MesCommandes.vue')
    },
    {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/404.vue')
    },
    {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue')
}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    const pagesProtegees = ['/commande', '/mes-commandes']

    if (pagesProtegees.includes(to.path) && !authStore.isAuthenticated) {
    next('/login')
    } else {
    next()
    }
})

router.beforeEach((to, from, next) => {
const authStore = useAuthStore()
const pagesProtegees = ['/commande', '/mes-commandes']
const pagesAdmin = ['/admin']

    if (pagesProtegees.includes(to.path) && !authStore.isAuthenticated) {
    next('/login')
    } else if (pagesAdmin.includes(to.path) && !authStore.isAdmin) {
    next('/')
    } else {
    next()
    }
})

export default router