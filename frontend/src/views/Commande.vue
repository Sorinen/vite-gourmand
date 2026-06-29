<template>
<div class="commande-page">
    <div class="commande-card">
        <h1>Passer une commande</h1>

        <div v-if="erreur" class="erreur">{{ erreur }}</div>
        <div v-if="succes" class="succes">{{ succes }}</div>

        <form @submit.prevent="passerCommande">
            <div class="champ">
                <label>Menu</label>
                <select v-model="menuId" required>
                    <option value="">Choisir un menu</option>
                    <option v-for="menu in menus" :key="menu.id" :value="menu.id">
                        {{ menu.titre }} — {{ menu.prix_base }}€/pers
                    </option>
                </select>
            </div>

            <div class="champ">
                <label>Date de prestation</label>
                <input type="date" v-model="datePrestation" required />
            </div>

            <div class="champ">
                <label>Heure de livraison</label>
                <input type="time" v-model="heureLivraison" required />
            </div>

            <div class="champ">
                <label>Adresse de livraison</label>
                <input type="text" v-model="adresseLivraison" required placeholder="123 rue exemple" />
            </div>

            <div class="champ">
                <label>Ville</label>
                <input type="text" v-model="ville" required placeholder="Bordeaux" />
            </div>

            <div class="champ">
                <label>Nombre de personnes</label>
                <input type="number" v-model="nombrePersonnes" required min="1" />
            </div>

            <div class="champ">
                <label>Mode de contact</label>
                <select v-model="modeContact">
                    <option value="email">Email</option>
                    <option value="telephone">Téléphone</option>
                </select>
            </div>

            <div class="champ checkbox">
                <label>
                    <input type="checkbox" v-model="pretMateriel" />
                    Je fournis le matériel (tables, chaises)
                </label>
            </div>

            <div class="resume" v-if="menuSelectionne">
                <h3>Résumé</h3>
                <p>Menu : {{ menuSelectionne.titre }}</p>
                <p>Prix par personne : {{ menuSelectionne.prix_base }}€</p>
                <p>Minimum : {{ menuSelectionne.nombre_personnes_min }} personnes</p>
                <p class="total">Total estimé : {{ menuSelectionne.prix_base * nombrePersonnes }}€</p>
            </div>

            <button type="submit" :disabled="chargement">
                {{ chargement ? 'Envoi...' : 'Confirmer la commande' }}
            </button>
        </form>
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
    useRouter,
    useRoute
} from 'vue-router'
import {
    useAuthStore
} from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const menus = ref([])
const menuId = ref('')
const datePrestation = ref('')
const heureLivraison = ref('')
const adresseLivraison = ref('')
const ville = ref('')
const nombrePersonnes = ref(1)
const modeContact = ref('email')
const pretMateriel = ref(false)
const erreur = ref('')
const succes = ref('')
const chargement = ref(false)

const menuSelectionne = computed(() => {
    return menus.value.find(m => m.id === Number(menuId.value))
})

onMounted(async () => {
    if (!authStore.isAuthenticated) {
        router.push('/login')
        return
    }
    try {
        const res = await api.get('/menu/')
        menus.value = res.data
        // Pré-remplir le menu si passé en paramètre URL
        if (route.query.menu) {
            menuId.value = Number(route.query.menu)
        }
    } catch (e) {
        console.error('Erreur menus', e)
    }
})

async function passerCommande() {
    erreur.value = ''
    succes.value = ''
    chargement.value = true

    if (!menuSelectionne.value) {
        erreur.value = 'Veuillez choisir un menu.'
        chargement.value = false
        return
    }

    try {
        await api.post('/commandes/', {
            date_prestation: datePrestation.value,
            heure_livraison: heureLivraison.value,
            adresse_livraison: adresseLivraison.value,
            nombre_personnes: Number(nombrePersonnes.value),
            prix_menu: menuSelectionne.value.prix_base * Number(nombrePersonnes.value),
            prix_livraison: ville.value.toLowerCase() === 'bordeaux' ? 0 : 15,
            prix_total: (menuSelectionne.value.prix_base * Number(nombrePersonnes.value)) + (ville.value.toLowerCase() === 'bordeaux' ? 0 : 15),
            statut: 'en_attente',
            mode_contact: modeContact.value,
            pret_materiel: pretMateriel.value,
            motif_annulation: null,
            utilisateur_id: authStore.user.id,
            menu_id: Number(menuId.value)
        })
        succes.value = 'Commande envoyée avec succès !'
        setTimeout(() => router.push('/mes-commandes'), 2000)
    } catch (e) {
        erreur.value = 'Erreur lors de la commande.'
        console.error(e)
    } finally {
        chargement.value = false
    }
}
</script>

<style scoped>
.commande-page {
    display: flex;
    justify-content: center;
    padding: 3rem 2rem;
}

.commande-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 600px;
}

h1 {
    color: #1D9E75;
    margin-bottom: 1.5rem;
    text-align: center;
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
.champ select {
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

.resume {
    background: #f0f9f5;
    padding: 1rem;
    border-radius: 4px;
    margin: 1rem 0;
    border-left: 4px solid #1D9E75;
}

.resume h3 {
    color: #1D9E75;
    margin-bottom: 0.5rem;
}

.total {
    font-weight: bold;
    color: #085041;
    margin-top: 0.5rem;
}

button {
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

button:disabled {
    opacity: 0.6;
}

.erreur {
    background: #fee;
    color: #c00;
    padding: 0.7rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    text-align: center;
}

.succes {
    background: #efe;
    color: #060;
    padding: 0.7rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    text-align: center;
}

@media (max-width: 768px) {
    .commande-page {
        padding: 1rem;
    }
}
</style>
