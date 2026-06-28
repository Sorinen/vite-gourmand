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
        <RouterLink to="/admin" v-if="authStore.isAdmin">Dashboard</RouterLink>
        <RouterLink to="/employe" v-if="authStore.isEmploye">Dashboard</RouterLink>
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

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #085041;
    color: white;
    flex-wrap: wrap;
    gap: 1rem;
}

.navbar-brand a {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
}

.navbar-links {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
}

.navbar-links a {
    color: white;
    text-decoration: none;
    font-size: 0.95rem;
}

.navbar-links a:hover {
    text-decoration: underline;
}

.navbar-links button {
    background: white;
    color: #085041;
    border: none;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
}

.navbar-links .bouton {
    background: #1D9E75;
    color: white;
}

.navbar-links .btn {
    background: #ee2b2b;
    color: white;
}

@media (max-width: 768px) {
    .navbar {
    padding: 1rem;
    flex-direction: column;
    align-items: flex-start;
    }

    .navbar-links {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    }

    .navbar-links a,
    .navbar-links button {
    width: 100%;
    text-align: left;
    }
}

</style>
