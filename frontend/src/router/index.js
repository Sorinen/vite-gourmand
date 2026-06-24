import { createRouter, createWebHistory } from 'vue-router'

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
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router