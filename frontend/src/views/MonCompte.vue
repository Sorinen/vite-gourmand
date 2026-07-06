<template>
  <div class="compte-page">
    <div class="compte-card">
      <h1>Mon compte</h1>

      <div v-if="succes" class="succes">{{ succes }}</div>
      <div v-if="erreur" class="erreur">{{ erreur }}</div>

      <form @submit.prevent="sauvegarder">
        <div class="champ">
          <label>Prénom</label>
          <input type="text" v-model="form.prenom" required />
        </div>
        <div class="champ">
          <label>Nom</label>
          <input type="text" v-model="form.nom" required />
        </div>
        <div class="champ">
          <label>Email</label>
          <input type="email" :value="user.email" disabled class="disabled" />
          <p class="aide">L'email ne peut pas être modifié.</p>
        </div>
        <div class="champ">
          <label>Téléphone</label>
          <input type="tel" v-model="form.telephone" placeholder="0692 00 00 00" />
        </div>
        <div class="champ">
          <label>Adresse postale</label>
          <input type="text" v-model="form.adresse_postale" placeholder="123 rue exemple, Bordeaux" />
        </div>
        <button type="submit" :disabled="chargement">
          {{ chargement ? 'Enregistrement...' : 'Sauvegarder les modifications' }}
        </button>
      </form>

      <div class="liens">
        <RouterLink to="/mes-commandes">Mes commandes</RouterLink>
        <RouterLink to="/mot-de-passe-oublie">Changer mon mot de passe</RouterLink>
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
const user = ref({})
const form = ref({ prenom: '', nom: '', telephone: '', adresse_postale: '' })
const succes = ref('')
const erreur = ref('')
const chargement = ref(false)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  try {
    const res = await api.get(`/utilisateurs/${authStore.user.id}`)
    user.value = res.data
    form.value = {
      prenom: res.data.prenom || '',
      nom: res.data.nom || '',
      telephone: res.data.telephone || '',
      adresse_postale: res.data.adresse_postale || ''
    }
  } catch (e) {
    erreur.value = 'Erreur lors du chargement des informations.'
  }
})

async function sauvegarder() {
  erreur.value = ''
  succes.value = ''
  chargement.value = true
  try {
    const res = await api.patch(`/utilisateurs/${authStore.user.id}`, form.value)
    authStore.setUser({ ...authStore.user, ...res.data })
    succes.value = 'Informations mises à jour avec succès !'
  } catch (e) {
    erreur.value = e.response?.data?.detail || 'Erreur lors de la sauvegarde.'
  } finally {
    chargement.value = false
  }
}
</script>

<style scoped>
.compte-page {
  display: flex;
  justify-content: center;
  padding: 3rem 2rem;
}
.compte-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 500px;
}
h1 { color: #1D9E75; margin-bottom: 1.5rem; text-align: center; }
.champ { margin-bottom: 1rem; }
.champ label { display: block; margin-bottom: 0.3rem; font-weight: bold; }
.champ input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}
.disabled { background: #f5f5f5; color: #999; cursor: not-allowed; }
.aide { font-size: 0.8rem; color: #888; margin-top: 0.3rem; }
button {
  width: 100%;
  padding: 0.8rem;
  background: #1D9E75;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 0.5rem;
}
button:disabled { opacity: 0.6; }
.succes { background: #efe; color: #060; padding: 0.7rem; border-radius: 4px; margin-bottom: 1rem; text-align: center; }
.erreur { background: #fee; color: #c00; padding: 0.7rem; border-radius: 4px; margin-bottom: 1rem; text-align: center; }
.liens {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1.5rem;
  border-top: 1px solid #eee;
  padding-top: 1rem;
}
.liens a { color: #1D9E75; text-decoration: none; font-size: 0.95rem; }
.liens a:hover { text-decoration: underline; }
@media (max-width: 768px) {
  .compte-page { padding: 1rem; }
}
</style>
