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
      <div class="filtres-commandes">
        <select v-model="filtreStatut">
          <option value="">Tous les statuts</option>
          <option value="en_attente">En attente</option>
          <option value="accepte">Accepté</option>
          <option value="en_preparation">En préparation</option>
          <option value="en_cours_livraison">En cours de livraison</option>
          <option value="livre">Livré</option>
          <option value="en_attente_retour_materiel">Attente retour matériel</option>
          <option value="terminee">Terminée</option>
          <option value="annulee">Annulée</option>
        </select>
      </div>
      <div v-if="commandesFiltrees.length > 0">
        <div class="commande-card" v-for="commande in commandesFiltrees" :key="commande.id">
          <div class="commande-header">
            <span class="commande-id">#{{ commande.id }}</span>
            <span class="menu-nom">{{ getNomMenu(commande.menu_id) }}</span>
            <span :class="['statut-badge', commande.statut]">{{ formatStatut(commande.statut) }}</span>
            <span>{{ commande.date_prestation }}</span>
            <span>{{ commande.nombre_personnes }} pers.</span>
            <span>{{ commande.prix_total }}€</span>
          </div>
          <div class="commande-statut">
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
          <div v-if="contactReponse === c.id" class="reponse-form">
            <textarea v-model="texteReponse" rows="4" placeholder="Votre réponse..."></textarea>
            <div class="reponse-actions">
              <button @click="envoyerReponse(c)" class="btn-valider">📧 Envoyer</button>
              <button @click="contactReponse = null" class="btn-annuler">Annuler</button>
            </div>
          </div>
          <div class="contact-actions">
            <button @click="ouvrirReponse(c.id)" class="btn-repondre">✉️ Répondre</button>
            <button @click="supprimerContact(c.id)" class="btn-refuser">🗑️ Supprimer</button>
          </div>
        </div>
      </div>
      <p v-else class="vide">✅ Aucun message de contact.</p>
    </div>

    <div class="employes-section">
      <h2>Gestion des employés</h2>

      <div class="creer-employe">
        <h3>Créer un compte employé</h3>
        <div v-if="succesEmploye" class="succes">{{ succesEmploye }}</div>
        <div v-if="erreurEmploye" class="erreur">{{ erreurEmploye }}</div>
        <form @submit.prevent="creerEmploye">
          <div class="form-grid">
            <div class="champ">
              <label>Prénom</label>
              <input type="text" v-model="nouveauEmploye.prenom" required />
            </div>
            <div class="champ">
              <label>Nom</label>
              <input type="text" v-model="nouveauEmploye.nom" required />
            </div>
            <div class="champ">
              <label>Email</label>
              <input type="email" v-model="nouveauEmploye.email" required />
            </div>
            <div class="champ">
              <label>Mot de passe temporaire</label>
              <input type="text" v-model="nouveauEmploye.mot_de_passe" required placeholder="À communiquer en personne" />
            </div>
          </div>
          <button type="submit" class="btn-creer" :disabled="chargementEmploye">
            {{ chargementEmploye ? 'Création...' : '➕ Créer le compte employé' }}
          </button>
        </form>
      </div>

      <div class="liste-employes" v-if="employes.length > 0">
        <h3>Comptes employés</h3>
        <div class="employe-card" v-for="e in employes" :key="e.id">
          <div class="employe-info">
            <span class="employe-nom">{{ e.prenom }} {{ e.nom }}</span>
            <span class="employe-email">{{ e.email }}</span>
            <span :class="['badge-actif', e.actif ? 'actif' : 'inactif']">
              {{ e.actif ? '✅ Actif' : '🚫 Désactivé' }}
            </span>
          </div>
          <button
            @click="toggleActif(e)"
            :class="e.actif ? 'btn-desactiver' : 'btn-activer'"
          >
            {{ e.actif ? 'Désactiver' : 'Réactiver' }}
          </button>
        </div>
      </div>
      <p v-else class="vide">Aucun employé.</p>
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
          <textarea v-model="motifAnnulation" rows="4" placeholder="Expliquez le motif..."></textarea>
        </div>
        <button @click="confirmerAnnulation" class="btn-confirmer-annulation" :disabled="!motifAnnulation.trim()">
          Confirmer l'annulation
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const stats = ref([])
const commandes = ref([])
const avis = ref([])
const contacts = ref([])
const menus = ref([])
const employes = ref([])
const contactReponse = ref(null)
const texteReponse = ref('')
const commandeAAnnuler = ref(null)
const motifAnnulation = ref('')
const modeContactAnnulation = ref('appel')
const filtreStatut = ref('')
const succesEmploye = ref('')
const erreurEmploye = ref('')
const chargementEmploye = ref(false)
const nouveauEmploye = ref({ prenom: '', nom: '', email: '', mot_de_passe: '' })

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

const commandesFiltrees = computed(() => {
  if (!filtreStatut.value) return commandes.value
  return commandes.value.filter(c => c.statut === filtreStatut.value)
})

function onChangeStatut(commande) {
  if (commande.statut === 'annulee') {
    commandeAAnnuler.value = commande
    motifAnnulation.value = ''
    modeContactAnnulation.value = 'appel'
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
    alert("Erreur lors de l'annulation")
  }
}

async function creerEmploye() {
  erreurEmploye.value = ''
  succesEmploye.value = ''
  chargementEmploye.value = true
  try {
    await api.post('/utilisateurs/admin/creer-employe', nouveauEmploye.value)
    succesEmploye.value = `Compte créé pour ${nouveauEmploye.value.prenom}. Un mail de notification a été envoyé.`
    nouveauEmploye.value = { prenom: '', nom: '', email: '', mot_de_passe: '' }
    const res = await api.get('/utilisateurs/admin/employes')
    employes.value = res.data
  } catch (e) {
    erreurEmploye.value = e.response?.data?.detail || "Erreur lors de la création"
  } finally {
    chargementEmploye.value = false
  }
}

async function toggleActif(employe) {
  try {
    await api.patch(`/utilisateurs/admin/employes/${employe.id}/actif`, { actif: !employe.actif })
    employe.actif = !employe.actif
  } catch (e) {
    alert("Erreur lors de la modification")
  }
}

onMounted(async () => {
  if (!authStore.isAdmin) {
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
    const res = await api.get('/admin/stats/commandes-par-menu')
    stats.value = res.data
  } catch (e) {
    console.error('Erreur stats', e)
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
  try {
    const res = await api.get('/contact/')
    contacts.value = res.data
  } catch (e) {
    console.error('Erreur contacts', e)
  }
  try {
    const res = await api.get('/utilisateurs/admin/employes')
    employes.value = res.data
  } catch (e) {
    console.error('Erreur employes', e)
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

function ouvrirReponse(id) {
  contactReponse.value = id
  texteReponse.value = ''
}

async function envoyerReponse(contact) {
  if (!texteReponse.value.trim()) return
  const mailtoLink = `mailto:${contact.email}?subject=Réponse à votre message - Vite & Gourmand&body=${encodeURIComponent(texteReponse.value)}`
  window.open(mailtoLink)
  contactReponse.value = null
  texteReponse.value = ''
}

async function supprimerContact(id) {
  if (!confirm('Supprimer ce message ?')) return
  try {
    await api.delete(`/contact/${id}`)
    contacts.value = contacts.value.filter(c => c.id !== id)
  } catch (e) {
    console.error('Erreur suppression contact', e)
  }
}
</script>

<style scoped>
.admin-page { max-width: 1200px; margin: 0 auto; padding: 2rem; }
h1 { color: #1D9E75; margin-bottom: 2rem; text-align: center; }
h2 { color: #085041; margin-bottom: 1.5rem; border-bottom: 2px solid #1D9E75; padding-bottom: 0.5rem; }
h3 { color: #085041; margin-bottom: 1rem; }
.nav-admin { display: flex; gap: 1rem; margin-bottom: 2rem; }
.btn-nav { background: #085041; color: white; padding: 0.7rem 1.5rem; border-radius: 4px; text-decoration: none; font-weight: bold; }
.stats-section { margin-bottom: 3rem; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1.5rem; }
.stat-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; border-top: 4px solid #1D9E75; }
.stat-card h3 { color: #085041; margin-bottom: 0.5rem; font-size: 0.95rem; }
.nombre { font-size: 1.5rem; font-weight: bold; color: #1D9E75; }
.ca { color: #666; font-size: 0.9rem; }
.commandes-section { margin-bottom: 3rem; }
.filtres-commandes { margin-bottom: 1rem; }
.filtres-commandes select { padding: 0.5rem 1rem; border: 1px solid #ccc; border-radius: 4px; font-size: 0.95rem; }
.commande-card { background: white; border-radius: 8px; padding: 1rem 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.commande-header { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; }
.commande-id { font-weight: bold; color: #1D9E75; }
.menu-nom { font-weight: bold; color: #085041; background: #f0f9f5; padding: 0.2rem 0.6rem; border-radius: 4px; }
.commande-statut select { padding: 0.4rem 0.8rem; border: 1px solid #ccc; border-radius: 4px; font-size: 0.9rem; }
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
.contacts-section { margin-bottom: 3rem; }
.contact-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem; }
.contact-header { display: flex; gap: 1.5rem; margin-bottom: 0.8rem; font-weight: bold; flex-wrap: wrap; }
.contact-nom { color: #085041; }
.contact-email { color: #1D9E75; }
.contact-tel { color: #666; }
.contact-message { color: #444; font-size: 0.95rem; border-left: 3px solid #1D9E75; padding-left: 1rem; margin-bottom: 1rem; }
.contact-actions { display: flex; gap: 1rem; margin-top: 1rem; }
.btn-repondre { background: #1D9E75; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; width: auto; }
.reponse-form { margin-top: 1rem; }
.reponse-form textarea { width: 100%; padding: 0.7rem; border: 1px solid #ccc; border-radius: 4px; font-size: 0.95rem; font-family: inherit; resize: vertical; }
.reponse-actions { display: flex; gap: 1rem; margin-top: 0.5rem; }
.btn-annuler { background: #666; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; width: auto; }
.employes-section { margin-bottom: 3rem; }
.creer-employe { background: #f0f9f5; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; border-left: 4px solid #1D9E75; }
.form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem; }
.champ { margin-bottom: 0; }
.champ label { display: block; margin-bottom: 0.3rem; font-weight: bold; font-size: 0.9rem; }
.champ input, .champ select, .champ textarea { width: 100%; padding: 0.6rem; border: 1px solid #ccc; border-radius: 4px; font-family: inherit; }
.btn-creer { background: #1D9E75; color: white; border: none; padding: 0.7rem 1.5rem; border-radius: 4px; cursor: pointer; font-size: 0.95rem; }
.btn-creer:disabled { opacity: 0.6; }
.employe-card { background: white; border-radius: 8px; padding: 1rem 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.employe-info { display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap; }
.employe-nom { font-weight: bold; color: #085041; }
.employe-email { color: #1D9E75; }
.badge-actif { padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.85rem; }
.actif { background: #d4edda; color: #155724; }
.inactif { background: #f8d7da; color: #721c24; }
.btn-desactiver { background: #dc3545; color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 4px; cursor: pointer; width: auto; }
.btn-activer { background: #1D9E75; color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 4px; cursor: pointer; width: auto; }
.succes { background: #efe; color: #060; padding: 0.6rem; border-radius: 4px; margin-bottom: 1rem; }
.erreur { background: #fee; color: #c00; padding: 0.6rem; border-radius: 4px; margin-bottom: 1rem; }
.vide { color: #666; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal { background: white; padding: 2rem; border-radius: 8px; max-width: 450px; width: 90%; position: relative; }
.modal h2 { color: #dc3545; margin-bottom: 0.5rem; }
.modal-close { position: absolute; top: 1rem; right: 1rem; background: none; border: none; font-size: 1.2rem; cursor: pointer; width: auto; color: #333; }
.info { color: #888; font-size: 0.85rem; margin-bottom: 1.5rem; }
.btn-confirmer-annulation { width: 100%; padding: 0.7rem; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 0.5rem; }
.btn-confirmer-annulation:disabled { opacity: 0.5; }
@media (max-width: 768px) {
  .admin-page { padding: 1rem; }
  .commande-card, .employe-card { flex-direction: column; align-items: flex-start; }
  .commande-header, .employe-info { flex-direction: column; gap: 0.5rem; }
  .stats-grid, .form-grid { grid-template-columns: 1fr; }
  .contact-actions, .avis-actions, .reponse-actions { flex-direction: column; }
}
</style>
