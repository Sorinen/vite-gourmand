<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <RouterLink to="/">Vite & Gourmand</RouterLink>
    </div>
    <button class="burger" @click="menuOuvert = !menuOuvert">☰</button>
    <div :class="['navbar-links', { ouvert: menuOuvert }]">
      <RouterLink to="/" @click="menuOuvert = false">Accueil</RouterLink>
      <RouterLink to="/menus" @click="menuOuvert = false">Nos Menus</RouterLink>
      <RouterLink to="/contact" @click="menuOuvert = false">Contact</RouterLink>
      <RouterLink to="/mes-commandes" v-if="authStore.isAuthenticated" @click="menuOuvert = false">Mes commandes</RouterLink>
      <RouterLink to="/mon-compte" v-if="authStore.isAuthenticated" @click="menuOuvert = false">Mon compte</RouterLink>
      <RouterLink to="/avis" v-if="authStore.isAuthenticated && !authStore.isAdmin && !authStore.isEmploye" @click="menuOuvert = false">Laisser un avis</RouterLink>
      <RouterLink to="/admin" v-if="authStore.isAdmin" @click="menuOuvert = false">Dashboard</RouterLink>
      <RouterLink to="/employe" v-if="authStore.isEmploye && !authStore.isAdmin" @click="menuOuvert = false">Dashboard</RouterLink>
      <button class="bouton" v-if="!authStore.isAuthenticated" @click="router.push('/login'); menuOuvert = false">Connexion</button>
      <button class="btn-logout" v-if="authStore.isAuthenticated" @click="logout">Déconnexion</button>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const menuOuvert = ref(false)

function logout() {
  authStore.logout()
  router.push('/')
  menuOuvert.value = false
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #085041;
  color: white;
  flex-wrap: wrap;
  gap: 1rem;
  position: relative;
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
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}
.bouton {
  background: #1D9E75;
  color: white;
}
.btn-logout {
  background: #ee2b2b;
  color: white;
}
.burger {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
    flex-direction: row;
    align-items: center;
  }
  .burger {
    display: block;
  }
  .navbar-links {
    display: none;
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding-top: 0.5rem;
  }
  .navbar-links.ouvert {
    display: flex;
  }
  .navbar-links a,
  .navbar-links button {
    width: 100%;
    text-align: left;
  }
}
</style>
