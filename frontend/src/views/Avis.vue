<template>
  <div class="avis-page">
    <div class="avis-card">
      <h1>Laisser un avis</h1>

      <div v-if="succes" class="succes">{{ succes }}</div>
      <div v-if="erreur" class="erreur">{{ erreur }}</div>

      <div v-if="mesCommandes.length === 0 && !chargement" class="info">
        Vous n'avez pas de commande terminée sans avis.
      </div>

      <form v-else @submit.prevent="soumettreAvis">
        <div class="champ">
          <label>Note</label>
          <div class="etoiles">
            <span v-for="n in 5" :key="n" @click="note = n" :class="['etoile', { active: n <= note }]">★</span>
          </div>
        </div>

        <div class="champ">
          <label>Commande</label>
          <select v-model="commandeId" required>
            <option value="">Choisir une commande</option>
            <option v-for="c in mesCommandes" :key="c.id" :value="c.id">
              Commande #{{ c.id }} — {{ c.date_prestation }}
            </option>
          </select>
        </div>

        <div class="champ">
          <label>Commentaire</label>
          <textarea v-model="commentaire" rows="5" placeholder="Votre avis..."></textarea>
        </div>

        <button type="submit" :disabled="chargement">
          {{ chargement ? 'Envoi...' : 'Envoyer mon avis' }}
        </button>
      </form>
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

const note = ref(0)
const commentaire = ref('')
const commandeId = ref('')
const mesCommandes = ref([])
const avisExistants = ref([])
const succes = ref('')
const erreur = ref('')
const chargement = ref(false)

const commandeSelectionnee = computed(() => {
  return mesCommandes.value.find(c => c.id === Number(commandeId.value))
})

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  try {
    const resAvis = await api.get('/avis/')
    avisExistants.value = resAvis.data.filter(a => a.utilisateur_id === authStore.user.id)
  } catch (e) {
    console.error('Erreur avis', e)
  }
  try {
    const res = await api.get('/commandes/')
    const commandesTerminees = res.data.filter(c =>
      c.utilisateur_id === authStore.user.id && c.statut === 'terminee'
    )
    // Exclure les commandes qui ont déjà un avis
    mesCommandes.value = commandesTerminees.filter(c =>
      !avisExistants.value.some(a => a.commande_id === c.id)
    )
  } catch (e) {
    console.error('Erreur commandes', e)
  }
})

async function soumettreAvis() {
  erreur.value = ''
  succes.value = ''

  if (note.value === 0) {
    erreur.value = 'Veuillez choisir une note.'
    return
  }

  if (!commandeId.value) {
    erreur.value = 'Veuillez choisir une commande.'
    return
  }

  chargement.value = true
  try {
    await api.post('/avis/', {
      note: note.value,
      commentaire: commentaire.value,
      statut: 'en_attente',
      commande_id: Number(commandeId.value),
      utilisateur_id: authStore.user.id,
      menu_id: commandeSelectionnee.value ? commandeSelectionnee.value.menu_id : null
    })
    succes.value = 'Votre avis a été envoyé, il sera visible après validation.'
    // Retirer la commande de la liste
    mesCommandes.value = mesCommandes.value.filter(c => c.id !== Number(commandeId.value))
    note.value = 0
    commentaire.value = ''
    commandeId.value = ''
  } catch (e) {
    erreur.value = "Erreur lors de l'envoi de l'avis."
  } finally {
    chargement.value = false
  }
}
</script>

<style scoped>
.avis-page {
  display: flex;
  justify-content: center;
  padding: 3rem 2rem;
}

.avis-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
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

.champ select,
.champ textarea {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

.etoiles {
  display: flex;
  gap: 0.5rem;
  font-size: 2rem;
}

.etoile {
  cursor: pointer;
  color: #ccc;
}

.etoile.active {
  color: #f5a623;
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

.info {
  background: #f0f9f5;
  color: #085041;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
  border-left: 4px solid #1D9E75;
}

.succes {
  background: #efe;
  color: #060;
  padding: 0.7rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
}

.erreur {
  background: #fee;
  color: #c00;
  padding: 0.7rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  text-align: center;
}
</style>
