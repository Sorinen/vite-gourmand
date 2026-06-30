<template>
  <div class="mes-commandes-page">
    <h1>Mes commandes</h1>
    <div v-if="commandes.length > 0" class="commandes-grid">
      <div class="commande-card" v-for="commande in commandes" :key="commande.id">
        <div class="commande-header">
          <span class="commande-id">#{{ commande.id }}</span>
          <span :class="['statut', commande.statut]">{{ formatStatut(commande.statut) }}</span>
        </div>
        <p><strong>Menu :</strong> {{ getNomMenu(commande.menu_id) }}</p>
        <p><strong>Date :</strong> {{ commande.date_prestation }}</p>
        <p><strong>Adresse :</strong> {{ commande.adresse_livraison }}</p>
        <p><strong>Personnes :</strong> {{ commande.nombre_personnes }}</p>
        <p><strong>Total :</strong> {{ commande.prix_total }}€</p>

        <div class="actions">
          <button @click="voirSuivi(commande.id)" class="btn-suivi">📋 Suivi</button>
          <button v-if="commande.statut === 'en_attente'" @click="ouvrirModification(commande)" class="btn-modifier">✏️ Modifier</button>
          <button v-if="commande.statut === 'en_attente'" @click="annuler(commande.id)" class="btn-annuler">❌ Annuler</button>
        </div>
      </div>
    </div>
    <p v-else class="vide">Vous n'avez pas encore de commande.</p>

    <!-- Modal suivi -->
    <div class="modal-overlay" v-if="commandeSuivi" @click.self="fermerSuivi">
      <div class="modal">
        <button class="modal-close" @click="fermerSuivi">✕</button>
        <h2>Suivi de la commande #{{ commandeSuivi }}</h2>
        <div v-if="historique.length > 0" class="timeline">
          <div class="timeline-item" v-for="h in historique" :key="h.id">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-statut">{{ formatStatut(h.statut) }}</span>
              <span class="timeline-date">{{ formatDate(h.date_changement) }}</span>
            </div>
          </div>
        </div>
        <p v-else>Aucun historique disponible.</p>
      </div>
    </div>

    <!-- Modal modification -->
    <div class="modal-overlay" v-if="commandeModification" @click.self="fermerModification">
      <div class="modal">
        <button class="modal-close" @click="fermerModification">✕</button>
        <h2>Modifier la commande #{{ commandeModification.id }}</h2>
        <p class="info-modal">Le menu ne peut pas être modifié.</p>

        <div v-if="erreurModif" class="erreur">{{ erreurModif }}</div>
        <div v-if="succesModif" class="succes">{{ succesModif }}</div>

        <form @submit.prevent="enregistrerModification">
          <div class="champ">
            <label>Date de prestation</label>
            <input type="date" v-model="modifForm.date_prestation" required />
          </div>
          <div class="champ">
            <label>Heure de livraison</label>
            <input type="time" v-model="modifForm.heure_livraison" required />
          </div>
          <div class="champ">
            <label>Adresse de livraison</label>
            <input type="text" v-model="modifForm.adresse_livraison" required />
          </div>
          <div class="champ">
            <label>Nombre de personnes</label>
            <input type="number" v-model.number="modifForm.nombre_personnes" required min="1" />
          </div>
          <div class="champ checkbox">
            <label>
              <input type="checkbox" v-model="modifForm.pret_materiel" />
              Louer le matériel — +15€
            </label>
          </div>
          <button type="submit" class="btn-valider-modif" :disabled="chargementModif">
            {{ chargementModif ? 'Enregistrement...' : 'Enregistrer les modifications' }}
          </button>
        </form>
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
const menus = ref([])
const commandeSuivi = ref(null)
const historique = ref([])
const commandeModification = ref(null)
const modifForm = ref({})
const erreurModif = ref('')
const succesModif = ref('')
const chargementModif = ref(false)

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

function formatDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' })
}

function getNomMenu(menuId) {
  const menu = menus.value.find(m => m.id === menuId)
  return menu ? menu.titre : 'Menu inconnu'
}

async function voirSuivi(commandeId) {
  commandeSuivi.value = commandeId
  try {
    const res = await api.get(`/commandes/${commandeId}/historique`)
    historique.value = res.data
  } catch (e) {
    console.error('Erreur historique', e)
    historique.value = []
  }
}

function fermerSuivi() {
  commandeSuivi.value = null
  historique.value = []
}

function ouvrirModification(commande) {
  commandeModification.value = commande
  modifForm.value = {
    date_prestation: commande.date_prestation,
    heure_livraison: commande.heure_livraison,
    adresse_livraison: commande.adresse_livraison,
    nombre_personnes: commande.nombre_personnes,
    pret_materiel: commande.pret_materiel
  }
  erreurModif.value = ''
  succesModif.value = ''
}

function fermerModification() {
  commandeModification.value = null
}

async function enregistrerModification() {
  erreurModif.value = ''
  succesModif.value = ''
  chargementModif.value = true
  try {
    const res = await api.put(`/commandes/${commandeModification.value.id}`, modifForm.value)
    const index = commandes.value.findIndex(c => c.id === commandeModification.value.id)
    if (index !== -1) commandes.value[index] = res.data
    succesModif.value = 'Commande modifiée avec succès !'
    setTimeout(() => fermerModification(), 1500)
  } catch (e) {
    erreurModif.value = e.response?.data?.detail || 'Erreur lors de la modification.'
  } finally {
    chargementModif.value = false
  }
}

async function annuler(commandeId) {
  if (!confirm('Êtes-vous sûr de vouloir annuler cette commande ?')) return
  try {
    await api.delete(`/commandes/${commandeId}`)
    const commande = commandes.value.find(c => c.id === commandeId)
    if (commande) commande.statut = 'annulee'
  } catch (e) {
    alert(e.response?.data?.detail || "Erreur lors de l'annulation.")
  }
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  try {
    const res = await api.get('/commandes/')
    commandes.value = res.data.filter(c => c.utilisateur_id === authStore.user.id)
  } catch (e) {
    console.error('Erreur commandes', e)
  }
  try {
    const res = await api.get('/menu/')
    menus.value = res.data
  } catch (e) {
    console.error('Erreur menus', e)
  }
})
</script>

<style scoped>
.mes-commandes-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
h1 { color: #1D9E75; margin-bottom: 2rem; text-align: center; }
.commandes-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
.commande-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.commande-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.commande-id { font-weight: bold; font-size: 1.1rem; color: #1D9E75; }
.statut { padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: bold; }
.en_attente { background: #fff3cd; color: #856404; }
.accepte { background: #d4edda; color: #155724; }
.en_preparation { background: #ffe5d0; color: #99450c; }
.en_cours_livraison { background: #cce5ff; color: #004085; }
.livre { background: #e2d9f3; color: #4a2c82; }
.en_attente_retour_materiel { background: #fde2cf; color: #99450c; }
.terminee { background: #d1ecf1; color: #0c5460; }
.annulee { background: #f8d7da; color: #721c24; }
.vide { text-align: center; color: #666; }

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.btn-suivi, .btn-modifier, .btn-annuler {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}
.btn-suivi { background: #085041; color: white; }
.btn-modifier { background: #1D9E75; color: white; }
.btn-annuler { background: #dc3545; color: white; }

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
  max-height: 80vh;
  overflow-y: auto;
}
.modal h2 { color: #1D9E75; margin-bottom: 1rem; }
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

.info-modal {
  color: #888;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

.champ { margin-bottom: 1rem; }
.champ label { display: block; margin-bottom: 0.3rem; font-weight: bold; }
.champ input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.checkbox input { width: auto; margin-right: 0.5rem; }

.btn-valider-modif {
  width: 100%;
  padding: 0.7rem;
  background: #1D9E75;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
}
.btn-valider-modif:disabled { opacity: 0.6; }

.erreur {
  background: #fee;
  color: #c00;
  padding: 0.6rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.85rem;
}
.succes {
  background: #efe;
  color: #060;
  padding: 0.6rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.85rem;
}

.timeline { position: relative; padding-left: 1.5rem; }
.timeline-item { position: relative; padding-bottom: 1.5rem; border-left: 2px solid #1D9E75; padding-left: 1.5rem; }
.timeline-item:last-child { border-left: 2px solid transparent; }
.timeline-dot { position: absolute; left: -7px; top: 0; width: 12px; height: 12px; background: #1D9E75; border-radius: 50%; }
.timeline-content { display: flex; flex-direction: column; gap: 0.2rem; }
.timeline-statut { font-weight: bold; color: #085041; }
.timeline-date { font-size: 0.85rem; color: #888; }

@media (max-width: 1024px) {
  .commandes-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .mes-commandes-page { padding: 1rem; }
  .commandes-grid { grid-template-columns: 1fr; }
  .actions { flex-direction: column; }
}
</style>
