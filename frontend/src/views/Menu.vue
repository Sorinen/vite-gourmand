<template>
<div class="menus-page">
    <h1>Nos Menus</h1>
    <div class="filtres">
        <select v-model="filtreTheme">
            <option value="">Tous les thèmes</option>
            <option v-for="theme in themes" :key="theme.id" :value="theme.id">
                {{ theme.libelle }}
            </option>
        </select>
        <select v-model="filtreRegime">
            <option value="">Tous les régimes</option>
            <option v-for="regime in regimes" :key="regime.id" :value="regime.id">
                {{ regime.libelle }}
            </option>
        </select>
    </div>
    <div class="menus-grid" v-if="menusFiltres.length > 0">
        <div class="menu-card" v-for="menu in menusFiltres" :key="menu.id">
            <h3>{{ menu.titre }}</h3>
            <p>{{ menu.description }}</p>
            <p class="prix">À partir de {{ menu.prix_base }}€ / personne</p>
            <p class="min">Minimum {{ menu.nombre_personnes_min }} personnes</p>
            <button @click="ouvrirModal(menu)" class="btn">Voir le menu</button>
        </div>
    </div>
    <p v-else>Aucun menu disponible.</p>

    <!-- Modal -->
    <div class="modal-overlay" v-if="menuSelectionne" @click.self="fermerModal">
        <div class="modal">
            <button class="modal-close" @click="fermerModal">✕</button>
            <h2>{{ menuSelectionne.titre }}</h2>
            <p>{{ menuSelectionne.description }}</p>
            <p class="prix">À partir de {{ menuSelectionne.prix_base }}€ / personne</p>
            <p class="min">Minimum {{ menuSelectionne.nombre_personnes_min }} personnes</p>
            <div class="modal-actions">
                <RouterLink v-if="authStore.isAuthenticated" to="/commande" class="btn-commander">
                    Commander ce menu
                </RouterLink>
                <RouterLink v-else to="/login" class="btn-commander">
                    Connectez-vous pour commander
                </RouterLink>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import {
    ref,
    computed,
    onMounted
} from 'vue'
import {
    useAuthStore
} from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()
const menus = ref([])
const themes = ref([])
const regimes = ref([])
const filtreTheme = ref('')
const filtreRegime = ref('')
const menuSelectionne = ref(null)

const menusFiltres = computed(() => {
    return menus.value.filter(menu => {
        const matchTheme = filtreTheme.value === '' || menu.theme_id === Number(filtreTheme.value)
        const matchRegime = filtreRegime.value === '' || menu.regime_id === Number(filtreRegime.value)
        return matchTheme && matchRegime
    })
})

function ouvrirModal(menu) {
    menuSelectionne.value = menu
}

function fermerModal() {
    menuSelectionne.value = null
}

onMounted(async () => {
    try {
        const res = await api.get('/menu/')
        menus.value = res.data
    } catch (e) {
        console.error('Erreur menus', e)
    }
    try {
        const res = await api.get('/themes/')
        themes.value = res.data
    } catch (e) {
        console.error('Erreur themes', e)
    }
    try {
        const res = await api.get('/regimes/')
        regimes.value = res.data
    } catch (e) {
        console.error('Erreur regimes', e)
    }
})
</script>

<style scoped>
.menus-page {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

h1 {
    color: #1D9E75;
    font-size: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}

.filtres {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
}

.filtres select {
    padding: 0.5rem 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
}

.menus-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
}

.menu-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.menu-card h3 {
    color: #1D9E75;
    margin-bottom: 0.5rem;
}

.prix {
    font-weight: bold;
    color: #333;
    margin: 0.5rem 0;
}

.min {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.btn {
    background: #1D9E75;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    border: none;
    cursor: pointer;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    max-width: 500px;
    width: 90%;
    position: relative;
}

.modal h2 {
    color: #1D9E75;
    margin-bottom: 1rem;
}

.modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    width: auto;
    color: #333;
}

.modal-actions {
    margin-top: 1.5rem;
}

.btn-commander {
    background: #1D9E75;
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: bold;
}
</style>
