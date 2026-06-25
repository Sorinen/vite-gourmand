<template>
<nav class="navbar">
    <div class="navbar-brand">
        <RouterLink to="/">Vite & Gourmand</RouterLink>
    </div>
    <div class="navbar-links">
        <RouterLink to="/">Accueil</RouterLink>
        <RouterLink to="/menus">Nos Menus</RouterLink>
        <RouterLink to="/contact">Contact</RouterLink>
        <RouterLink to="/mes-commandes" v-if="authStore.isAuthenticated">Mes commandes</RouterLink>
        <RouterLink to="/avis" v-if="authStore.isAuthenticated && !authStore.isAdmin">Laisser un avis</RouterLink>
        <button class="bouton" to="/login" v-if="!authStore.isAuthenticated" @click="router.push('/login')">Connexion</button>
        <button class="btn" v-if="authStore.isAuthenticated" @click="logout">Déconnexion</button>
    </div>
</nav>
</template>

<script setup>
import {
    useAuthStore
} from '../stores/auth'
import {
    useRouter
} from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
    authStore.logout()
    router.push('/')
}

</script>

<style scoped>
.navbar-links .bouton {
    background: #1D9E75;
    color: white;
}

.navbar-links .btn {
    background: #ee2b2b;
    color: white;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #085041;
    color: white;
}

.navbar-brand a {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
}

.navbar-links {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.navbar-links a {
    color: white;
    text-decoration: none;
    font-size: 1rem;
}

.navbar-links a:hover {
    text-decoration: underline;
}

.navbar-links button {
    background: white;
    color: #085041;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
}
</style>
