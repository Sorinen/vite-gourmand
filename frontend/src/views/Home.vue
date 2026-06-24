<template>
<div>
    <!-- Hero -->
    <section class="hero">
        <h1>Vite & Gourmand</h1>
        <p>Traiteur événementiel à La Réunion</p>
        <RouterLink to="/menus" class="btn-primary">Découvrir nos menus</RouterLink>
    </section>

    <!-- Menus en vedette -->
    <section class="featured">
        <h2>Nos menus</h2>
        <div class="menus-grid" v-if="menus.length > 0">
            <div class="menu-card" v-for="menu in menus" :key="menu.id">
                <h3>{{ menu.titre }}</h3>
                <p>{{ menu.description }}</p>
                <p class="prix">À partir de {{ menu.prix_base }}€ / personne</p>
                <RouterLink :to="`/menu/${menu.id}`" class="btn-secondary">Voir le menu</RouterLink>
            </div>
        </div>
        <p v-else>Aucun menu disponible pour le moment.</p>
    </section>

    <!-- Horaires -->
    <section class="horaires">
        <h2>Nos horaires</h2>
        <div v-if="horaires.length > 0">
            <div class="horaire-item" v-for="horaire in horaires" :key="horaire.id">
                <span class="jour">{{ horaire.jour }}</span>
                <span v-if="!horaire.ferme">{{ horaire.heure_ouverture }} - {{ horaire.heure_fermeture }}</span>
                <span v-else class="ferme">Fermé</span>
            </div>
        </div>
    </section>
</div>
</template>

<script setup>
import {
    ref,
    onMounted
} from 'vue'
import api from '../services/api'

const menus = ref([])
const horaires = ref([])

onMounted(async () => {
    try {
        const resMenus = await api.get('/menu/')
        menus.value = resMenus.data
    } catch (e) {
        console.error('Erreur chargement menus', e)
    }

    try {
        const resHoraires = await api.get('/horaire/')
        horaires.value = resHoraires.data
    } catch (e) {
        console.error('Erreur chargement horaires', e)
    }
})
</script>

<style scoped>
.hero {
    background-color: #1D9E75;
    color: white;
    text-align: center;
    padding: 5rem 2rem;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
}

.btn-primary {
    background: white;
    color: #1D9E75;
    padding: 0.8rem 2rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: bold;
}

.featured {
    padding: 3rem 2rem;
    text-align: center;
}

.featured h2 {
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #1D9E75;
}

.menus-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.menu-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    text-align: left;
}

.menu-card h3 {
    color: #1D9E75;
    margin-bottom: 0.5rem;
}

.prix {
    color: #666;
    margin: 1rem 0;
    font-weight: bold;
}

.btn-secondary {
    background: #1D9E75;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    text-decoration: none;
}

.horaires {
    background: #f0e6d3;
    padding: 3rem 2rem;
    text-align: center;
}

.horaires h2 {
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #1D9E75;
}

.horaire-item {
    display: flex;
    justify-content: space-between;
    max-width: 400px;
    margin: 0.5rem auto;
    padding: 0.5rem 1rem;
    background: white;
    border-radius: 4px;
}

.jour {
    font-weight: bold;
}

.ferme {
    color: #1D9E75;
}
</style>
