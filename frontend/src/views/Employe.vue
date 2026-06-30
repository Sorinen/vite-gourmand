<template>
  <div class="employe-page">
    <h1>Espace Employé</h1>

    <div class="commandes-section">
      <h2>Gestion des commandes</h2>
      <div v-if="commandes.length > 0">
        <div class="commande-card" v-for="commande in commandes" :key="commande.id">
          <div class="commande-header">
            <span class="commande-id">#{{ commande.id }}</span>
            <span class="menu-nom">{{ getNomMenu(commande.menu_id) }}</span>
            <span :class="['statut-badge', commande.statut]">{{ formatStatut(commande.statut) }}</span>
            <span>{{ commande.date_prestation }}</span>
            <span>{{ commande.nombre_personnes }} pers.</span>
            <span>{{ commande.prix_total }}€</span>
          </div>
          <select v-model="commande.statut" @change="changerStatut(commande)">
            <option value="en_attente">En attente</option>
            <option value="accepte">Accepté</option>
            <option value="en_preparation">En préparation</option>
            <option value="en_cours_livraison">En cours de livraison</option>
            <option value="livre">Livré</option>
            <option value="en_attente_retour_materiel">En attente du retour de matériel</option>
            <option value="terminee">Terminée</option>
            <option value="annulee">Annulée</option>
          </select>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const commandes = ref([])
const avis = ref([])
const menus = ref([])

const libellesStatuts = {
  en_attente: 'En attente',
  accepte: 'Accepté',
  en_preparation: 'En préparation',
  en_cours_livraison: 'En cours de livraison',
  livre: 'Livré',
  en_attente_retour_materiel: 'Attente retour matériel',
  terminee: 'Terminée',
  annulee: 'Annulée'
}

function formatStatut(statut) {
  return libellesStatuts[statut] || statut
}

function getNomMenu(menuId) {
  const menu = menus.value.find(m => m.id === menuId)
  return menu ? menu.titre : 'Menu inconnu'
}

onMounted(async () => {
  if (!authStore.isEmploye && !authStore.isAdmin) {
    router.push('/')
    return
  }
  try {
    const res = await api.get('/menu/')
    menus.value = res.data
  } catch (e) {
    console.error('Erreur menus', e)
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
})

async function changerStatut(commande) {
  try {
    await api.patch(`/commandes/${commande.id}/statut`, { statut: commande.statut })
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

<style scoped>
.employe-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
h1 { color: #1D9E75; margin-bottom: 2rem; text-align: center; }
h2 { color: #085041; margin-bottom: 1.5rem; border-bottom: 2px solid #1D9E75; padding-bottom: 0.5rem; }
.commandes-section { margin-bottom: 3rem; }
.commande-card { background: white; border-radius: 8px; padding: 1rem 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.commande-header { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }
.commande-id { font-weight: bold; color: #1D9E75; }
.menu-nom { font-weight: bold; color: #085041; background: #f0f9f5; padding: 0.2rem 0.6rem; border-radius: 4px; }
.statut-badge { padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }
.en_attente { background: #fff3cd; color: #856404; }
.accepte { background: #d4edda; color: #155724; }
.en_preparation { background: #ffe5d0; color: #99450c; }
.en_cours_livraison { background: #cce5ff; color: #004085; }
.livre { background: #e2d9f3; color: #4a2c82; }
.en_attente_retour_materiel { background: #fde2cf; color: #99450c; }
.terminee { background: #d1ecf1; color: #0c5460; }
.annulee { background: #f8d7da; color: #721c24; }
.avis-section { margin-bottom: 3rem; }
.avis-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem; }
.avis-header { display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-weight: bold; }
.avis-actions { display: flex; gap: 1rem; margin-top: 1rem; }
.btn-valider { background: #1D9E75; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; width: auto; }
.btn-refuser { background: #dc3545; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; width: auto; }
@media (max-width: 768px) {
  .employe-page { padding: 1rem; }
  .commande-card { flex-direction: column; align-items: flex-start; }
  .commande-header { flex-direction: column; gap: 0.5rem; align-items: flex-start; }
  .avis-actions { flex-direction: column; }
}
</style>
