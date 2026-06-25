<template>
<div class="admin-menus-page">
    <h1>Gestion des menus</h1>
    <RouterLink to="/admin" class="btn-retour">← Dashboard</RouterLink>

    <button @click="afficherFormulaire = true" class="btn-ajouter">+ Ajouter un menu</button>

    <!-- Formulaire création/modification -->
    <div class="modal-overlay" v-if="afficherFormulaire" @click.self="fermerFormulaire">
        <div class="modal">
            <button class="modal-close" @click="fermerFormulaire">✕</button>
            <h2>{{ menuEnEdition ? 'Modifier le menu' : 'Nouveau menu' }}</h2>

            <div v-if="erreur" class="erreur">{{ erreur }}</div>

            <form @submit.prevent="sauvegarderMenu">
                <div class="champ">
                    <label>Titre</label>
                    <input type="text" v-model="form.titre" required />
                </div>
                <div class="champ">
                    <label>Description</label>
                    <textarea v-model="form.description" rows="3" required></textarea>
                </div>
                <div class="champ">
                    <label>Prix de base (€/pers)</label>
                    <input type="number" v-model="form.prix_base" required min="0" step="0.01" />
                </div>
                <div class="champ">
                    <label>Nombre de personnes minimum</label>
                    <input type="number" v-model="form.nombre_personnes_min" required min="1" />
                </div>
                <div class="champ">
                    <label>Thème</label>
                    <select v-model="form.theme_id" required>
                        <option v-for="theme in themes" :key="theme.id" :value="theme.id">
                            {{ theme.libelle }}
                        </option>
                    </select>
                </div>
                <div class="champ">
                    <label>Régime</label>
                    <select v-model="form.regime_id" required>
                        <option v-for="regime in regimes" :key="regime.id" :value="regime.id">
                            {{ regime.libelle }}
                        </option>
                    </select>
                </div>
                <div class="champ">
                    <label>Conditions</label>
                    <input type="text" v-model="form.conditions" />
                </div>
                <div class="champ">
                    <label>Stock disponible</label>
                    <input type="number" v-model="form.stock_disponible" min="0" />
                </div>
                <div class="champ checkbox">
                    <label>
                        <input type="checkbox" v-model="form.actif" />
                        Menu actif
                    </label>
                </div>
                <button type="submit" :disabled="chargement">
                    {{ chargement ? 'Sauvegarde...' : 'Sauvegarder' }}
                </button>
            </form>
        </div>
    </div>

    <!-- Liste des menus -->
    <div class="menus-liste" v-if="menus.length > 0">
        <div class="menu-item" v-for="menu in menus" :key="menu.id">
            <div class="menu-info">
                <h3>{{ menu.titre }}</h3>
                <p>{{ menu.prix_base }}€/pers — Min {{ menu.nombre_personnes_min }} pers.</p>
                <span :class="['badge', menu.actif ? 'actif' : 'inactif']">
                    {{ menu.actif ? 'Actif' : 'Inactif' }}
                </span>
            </div>
            <div class="menu-actions">
                <button @click="modifierMenu(menu)" class="btn-modifier">✏️ Modifier</button>
                <button @click="supprimerMenu(menu.id)" class="btn-supprimer">🗑️ Supprimer</button>
            </div>
        </div>
    </div>
    <p v-else>Aucun menu.</p>
</div>
</template>

<script setup>
import {
    ref,
    onMounted
} from 'vue'
import {
    useRouter
} from 'vue-router'
import {
    useAuthStore
} from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()

const menus = ref([])
const themes = ref([])
const regimes = ref([])
const afficherFormulaire = ref(false)
const menuEnEdition = ref(null)
const erreur = ref('')
const chargement = ref(false)

const form = ref({
    titre: '',
    description: '',
    prix_base: 0,
    nombre_personnes_min: 10,
    theme_id: '',
    regime_id: '',
    conditions: '',
    stock_disponible: 10,
    actif: true
})

onMounted(async () => {
    if (!authStore.isAdmin) {
        router.push('/')
        return
    }
    await chargerDonnees()
})

async function chargerDonnees() {
    try {
        const [resMenus, resThemes, resRegimes] = await Promise.all([
            api.get('/menu/'),
            api.get('/themes/'),
            api.get('/regimes/')
        ])
        menus.value = resMenus.data
        themes.value = resThemes.data
        regimes.value = resRegimes.data
    } catch (e) {
        console.error('Erreur chargement', e)
    }
}

function modifierMenu(menu) {
    menuEnEdition.value = menu
    form.value = {
        ...menu
    }
    afficherFormulaire.value = true
}

function fermerFormulaire() {
    afficherFormulaire.value = false
    menuEnEdition.value = null
    erreur.value = ''
    form.value = {
        titre: '',
        description: '',
        prix_base: 0,
        nombre_personnes_min: 10,
        theme_id: '',
        regime_id: '',
        conditions: '',
        stock_disponible: 10,
        actif: true
    }
}

async function sauvegarderMenu() {
    erreur.value = ''
    chargement.value = true
    try {
        if (menuEnEdition.value) {
            await api.put(`/menu/${menuEnEdition.value.id}`, form.value)
        } else {
            await api.post('/menu/', form.value)
        }
        await chargerDonnees()
        fermerFormulaire()
    } catch (e) {
        erreur.value = 'Erreur lors de la sauvegarde.'
    } finally {
        chargement.value = false
    }
}

async function supprimerMenu(id) {
    if (!confirm('Supprimer ce menu ?')) return
    try {
        await api.delete(`/menu/${id}`)
        await chargerDonnees()
    } catch (e) {
        console.error('Erreur suppression', e)
    }
}
</script>

<style scoped>
.admin-menus-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

h1 {
    color: #1D9E75;
    margin-bottom: 1rem;
    text-align: center;
}

.btn-retour {
    color: #1D9E75;
    text-decoration: none;
    display: inline-block;
    margin-bottom: 1rem;
}

.btn-ajouter {
    background: #1D9E75;
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    margin-bottom: 2rem;
    width: auto;
}

.menus-liste {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.menu-item {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.menu-info h3 {
    color: #085041;
    margin-bottom: 0.3rem;
}

.badge {
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.8rem;
}

.actif {
    background: #d4edda;
    color: #155724;
}

.inactif {
    background: #f8d7da;
    color: #721c24;
}

.menu-actions {
    display: flex;
    gap: 0.5rem;
}

.btn-modifier {
    background: #ffc107;
    color: #333;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    width: auto;
}

.btn-supprimer {
    background: #dc3545;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    width: auto;
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
    max-height: 90vh;
    overflow-y: auto;
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
}

.champ {
    margin-bottom: 1rem;
}

.champ label {
    display: block;
    margin-bottom: 0.3rem;
    font-weight: bold;
}

.champ input,
.champ select,
.champ textarea {
    width: 100%;
    padding: 0.7rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
}

.checkbox input {
    width: auto;
    margin-right: 0.5rem;
}

button[type="submit"] {
    width: 100%;
    padding: 0.8rem;
    background: #1D9E75;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 1rem;
}

.erreur {
    background: #fee;
    color: #c00;
    padding: 0.7rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}
</style>
