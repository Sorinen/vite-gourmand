<template>
  <div class="page">
    <div class="card">
      <h1>Nouveau mot de passe</h1>

      <div v-if="succes" class="succes">{{ succes }}</div>
      <div v-if="erreur" class="erreur">{{ erreur }}</div>

      <form v-if="!succes" @submit.prevent="reinitialiser">
        <div class="champ">
          <label>Nouveau mot de passe</label>
          <input type="password" v-model="nouveauMdp" required minlength="10" placeholder="••••••••••" />
          <p class="aide">10 caractères minimum, avec majuscule, minuscule, chiffre et caractère spécial.</p>
        </div>
        <div class="champ">
          <label>Confirmer le mot de passe</label>
          <input type="password" v-model="confirmationMdp" required placeholder="••••••••••" />
        </div>
        <button type="submit" :disabled="chargement">
          {{ chargement ? 'Validation...' : 'Réinitialiser' }}
        </button>
      </form>

      <p class="lien" v-if="succes">
        <RouterLink to="/login">Se connecter</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const token = ref('')
const nouveauMdp = ref('')
const confirmationMdp = ref('')
const succes = ref('')
const erreur = ref('')
const chargement = ref(false)

onMounted(() => {
  token.value = route.query.token || ''
  if (!token.value) {
    erreur.value = 'Lien invalide.'
  }
})

async function reinitialiser() {
  erreur.value = ''
  succes.value = ''

  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{10,}$/
  if (!regex.test(nouveauMdp.value)) {
    erreur.value = 'Le mot de passe doit contenir au moins 10 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.'
    return
  }

  if (nouveauMdp.value !== confirmationMdp.value) {
    erreur.value = 'Les mots de passe ne correspondent pas.'
    return
  }

  chargement.value = true
  try {
    await api.post('/auth/reinitialiser-mot-de-passe', {
      token: token.value,
      nouveau_mot_de_passe: nouveauMdp.value
    })
    succes.value = 'Votre mot de passe a été réinitialisé avec succès !'
  } catch (e) {
    erreur.value = e.response?.data?.detail || 'Erreur lors de la réinitialisation.'
  } finally {
    chargement.value = false
  }
}
</script>

<style scoped>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
}
.card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
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
.champ input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}
.aide {
  font-size: 0.8rem;
  color: #888;
  margin-top: 0.3rem;
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
.lien {
  text-align: center;
  margin-top: 1rem;
}
.lien a {
  color: #1D9E75;
}
</style>
