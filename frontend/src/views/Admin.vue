<template>
<div class="admin-page">
    <h1>Dashboard Admin</h1>
    <div class="nav-admin">
        <RouterLink to="/admin/menus" class="btn-nav">🍽️ Gérer les menus</RouterLink>
    </div>

    <div class="stats-section">
        <h2>Statistiques des commandes</h2>
        <div v-if="stats.length > 0" class="stats-grid">
            <div class="stat-card" v-for="stat in stats" :key="stat._id">
                <h3>{{ stat.menu_titre }}</h3>
                <p class="nombre">{{ stat.nombre_commandes }} commandes</p>
                <p class="ca">{{ stat.chiffre_affaires }}€ de CA</p>
            </div>
        </div>
        <p v-else>Aucune statistique disponible.</p>
    </div>

    <div class="commandes-section">
        <h2>Gestion des commandes</h2>
        <div v-if="commandes.length > 0">
            <div class="commande-card" v-for="commande in commandes" :key="commande.id">
                <div class="commande-header">
                    <span class="commande-id">#{{ commande.id }}</span>
                    <span>{{ commande.date_prestation }}</span>
                    <span>{{ commande.nombre_personnes }} pers.</span>
                    <span>{{ commande.prix_total }}€</span>
                </div>
                <div class="commande-statut">
                    <select v-model="commande.statut" @change="changerStatut(commande)">
                        <option value="en_attente">En attente</option>
                        <option value="confirmee">Confirmée</option>
                        <option value="terminee">Terminée</option>
                        <option value="annulee">Annulée</option>
                    </select>
                </div>
            </div>
        </div>
        <p v-else>Aucune commande.</p>
    </div>

    <div class="avis-section">
        <h2>Gestion des avis</h2>
        <div v-if="avis.length > 0">
            <div class="avis-card" v-for="a in avis" :key="a.id">
                <div class="avis-header">
                    <span>Note : {{ a.note }}/5</span>
                    <span :class="['statut', a.statut]">{{ a.statut }}</span>
                </div>
                <p>{{ a.commentaire }}</p>
                <div class="avis-actions">
                    <button @click="validerAvis(a.id)" class="btn-valider">✅ Valider</button>
                    <button @click="supprimerAvis(a.id)" class="btn-refuser">❌ Refuser</button>
                </div>
            </div>
        </div>
        <p v-else>Aucun avis en attente.</p>
    </div>

    <div class="contacts-section">
        <h2>Messages de contact</h2>
        <div v-if="contacts.length > 0">
            <div class="contact-card" v-for="c in contacts" :key="c.id">
                <div class="contact-header">
                    <span class="contact-nom">{{ c.nom }}</span>
                    <span class="contact-email">{{ c.email }}</span>
                    <span v-if="c.telephone" class="contact-tel">{{ c.telephone }}</span>
                </div>
                <p class="contact-message">{{ c.message }}</p>
            </div>
        </div>
        <p v-else class="vide">✅ Aucun message de contact.</p>
    </div>
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
const stats = ref([])
const commandes = ref([])
const avis = ref([])
const contacts = ref([])

onMounted(async () => {
    if (!authStore.isAdmin) {
        router.push('/')
        return
    }

    try {
        const res = await api.get('/admin/stats/commandes-par-menu')
        stats.value = res.data
    } catch (e) {
        console.error('Erreur stats', e)
    }

    try {
        const res = await api.get('/commandes/')
        commandes.value = res.data
    } catch (e) {
        console.error('Erreur commandes', e)
    }

    try {
        const res = await api.get('/avis/')
        avis.value = res.data.filter(a => a.statut === 'en_attente')
    } catch (e) {
        console.error('Erreur avis', e)
    }

    try {
        const res = await api.get('/contact/')
        contacts.value = res.data
    } catch (e) {
        console.error('Erreur contacts', e)
    }
})

async function changerStatut(commande) {
    try {
        await api.patch(`/commandes/${commande.id}/statut`, {
            statut: commande.statut
        })
    } catch (e) {
        console.error('Erreur changement statut', e)
    }
}

async function validerAvis(id) {
    try {
        await api.patch(`/avis/${id}/valider`)
        avis.value = avis.value.filter(a => a.id !== id)
    } catch (e) {
        console.error('Erreur validation avis', e)
    }
}

async function supprimerAvis(id) {
    try {
        await api.delete(`/avis/${id}`)
        avis.value = avis.value.filter(a => a.id !== id)
    } catch (e) {
        console.error('Erreur suppression avis', e)
    }
}
</script>

<style>
.admin-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

h1 {
    color: #1D9E75;
    margin-bottom: 2rem;
    text-align: center;
}

h2 {
    color: #085041;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #1D9E75;
    padding-bottom: 0.5rem;
}

.nav-admin {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.btn-nav {
    background: #085041;
    color: white;
    padding: 0.7rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: bold;
}

.stats-section {
    margin-bottom: 3rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
}

.stat-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
    border-top: 4px solid #1D9E75;
}

.stat-card h3 {
    color: #085041;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.nombre {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1D9E75;
}

.ca {
    color: #666;
    font-size: 0.9rem;
}

.commandes-section {
    margin-bottom: 3rem;
}

.commande-card {
    background: white;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.commande-header {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    flex-wrap: wrap;
}

.commande-id {
    font-weight: bold;
    color: #1D9E75;
}

.commande-statut select {
    padding: 0.4rem 0.8rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.9rem;
}

.avis-section {
    margin-bottom: 3rem;
}

.avis-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
}

.avis-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

.avis-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.btn-valider {
    background: #1D9E75;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    width: auto;
}

.btn-refuser {
    background: #dc3545;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    width: auto;
}

.contacts-section {
    margin-bottom: 3rem;
}

.contact-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
}

.contact-header {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 0.8rem;
    font-weight: bold;
    flex-wrap: wrap;
}

.contact-nom {
    color: #085041;
}

.contact-email {
    color: #1D9E75;
}

.contact-tel {
    color: #666;
}

.contact-message {
    color: #444;
    font-size: 0.95rem;
    border-left: 3px solid #1D9E75;
    padding-left: 1rem;
}

@media (max-width: 768px) {
    .admin-page {
        padding: 1rem;
    }

    .commande-card {
        flex-direction: column;
        align-items: flex-start;
    }

    .commande-header {
        flex-direction: column;
        gap: 0.5rem;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }
}
</style>
