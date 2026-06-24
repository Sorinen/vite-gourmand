<template>
<div class="menu-detail-page">
    <div v-if="menu">
    <div class="menu-header">
        <h1>{{ menu.titre }}</h1>
        <p class="description">{{ menu.description }}</p>
        <p class="prix">À partir de {{ menu.prix_base }}€ / personne</p>
        <p class="min">Minimum {{ menu.nombre_personnes_min }} personnes</p>
    </div>

    <div class="menu-actions">
        <RouterLink to="/menus" class="btn-retour">← Retour aux menus</RouterLink>
        <RouterLink v-if="authStore.isAuthenticated" to="/commande" class="btn-commander">
        Commander ce menu
        </RouterLink>
        <RouterLink v-else to="/login" class="btn-commander">
        Connectez-vous pour commander
        </RouterLink>
    </div>
    </div>
    <div v-else>
        <p>Chargement...</p>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const route = useRoute()
const authStore = useAuthStore()
const menu = ref(null)

onMounted(async () => {
try {
    const res = await api.get(`/menu/${route.params.id}`)
    menu.value = res.data
    } catch (e) {
    console.error('Erreur chargement menu', e)
    }
})
</script>

<style scoped>
.menu-detail-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

.menu-header {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

h1 {
    color: #1D9E75;
    font-size: 2rem;
    margin-bottom: 1rem;
}

.description {
    color: #555;
    margin-bottom: 1rem;
    line-height: 1.6;
}

.prix {
    font-size: 1.3rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 0.5rem;
}

.min {
    color: #666;
}

.menu-actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.btn-retour {
    padding: 0.8rem 1.5rem;
    border: 2px solid #1D9E75;
    color: #1D9E75;
    border-radius: 4px;
    text-decoration: none;
}

.btn-commander {
    padding: 0.8rem 1.5rem;
    background: #1D9E75;
    color: white;
    border-radius: 4px;
    text-decoration: none;
    font-weight: bold;
}
</style>