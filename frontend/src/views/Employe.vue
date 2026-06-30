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
          <select v-model="commande.statut" @change="onChangeStatut(commande)">
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

    <!-- Modal annulation -->
    <div class="modal-overlay" v-if="commandeAAnnuler" @click.self="annulerModalAnnulation">
      <div class="modal">
        <button class="modal-close" @click="annulerModalAnnulation">✕</button>
        <h2>Annuler la commande #{{ commandeAAnnuler.id }}</h2>
        <p class="info">Le client doit avoir été contacté avant l'annulation.</p>

        <div class="champ">
          <label>Mode de contact utilisé</label>
          <select v-model="modeContactAnnulation">
            <option value="appel">Appel téléphonique</option>
            <option value="mail">Email</option>
          </select>
        </div>

        <div class="champ">
          <label>Motif d'annulation</label>
          <textarea v-model="motifAnnulation" rows="4" placeholder="Expliquez le motif de l'annulation..."></textarea>
        </div>

        <button @click="confirmerAnnulation" class="btn-confirmer-annulation" :disabled="!motifAnnulation.trim()">
          Confirmer l'annulation
        </button>
      </div>
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
const commandeAAnnuler = ref(null)
const motifAnnulation = ref('')
const modeContactAnnulation = ref('appel')

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

function onChangeStatut(commande) {
  if (commande.statut === 'annulee') {
    commandeAAnnuler.value = commande
    motifAnnulation.value = ''
    modeContactAnnulation.value = 'appel'
    // On revient temporairement à l'ancien statut tant que pas confirmé
    commande.statut = commande._statutPrecedent || 'en_attente'
  } else {
    commande._statutPrecedent = commande.statut
    changerStatut(commande)
  }
}

function annulerModalAnnulation() {
  commandeAAnnuler.value = null
}

async function confirmerAnnulation() {
  if (!motifAnnulation.value.trim()) return
  try {
    await api.patch(`/commandes/${commandeAAnnuler.value.id}/statut`, {
      statut: 'annulee',
      motif_annulation: motifAnnulation.value,
      mode_contact: modeContactAnnulation.value
    })
    const c = commandes.value.find(c => c.id === commandeAAnnuler.value.id)
    if (c) c.statut = 'annulee'
    commandeAAnnuler.value = null
  } catch (e) {
    console.error('Erreur annulation', e)
    alert("Erreur lors de l'annulation")
  }
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
    commandes.value = res.data.map(c => ({ ...c, _statutPrecedent: c.statut }))
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
  max-width: 450px;
  width: 90%;
  position: relative;
}
.modal h2 { color: #dc3545; margin-bottom: 0.5rem; }
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
.info {
  color: #888;
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
}
.champ { margin-bottom: 1rem; }
.champ label { display: block; margin-bottom: 0.3rem; font-weight: bold; }
.champ select, .champ textarea {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
}
.btn-confirmer-annulation {
  width: 100%;
  padding: 0.7rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
}
.btn-confirmer-annulation:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 768px) {
  .employe-page { padding: 1rem; }
  .commande-card { flex-direction: column; align-items: flex-start; }
  .commande-header { flex-direction: column; gap: 0.5rem; align-items: flex-start; }
  .avis-actions { flex-direction: column; }
}
</style>
