<template>
  <div class="page">
    <div class="card">
      <h1>Mot de passe oublié</h1>
      <p class="texte">Saisissez votre email, vous recevrez un lien pour réinitialiser votre mot de passe.</p>

      <div v-if="succes" class="succes">{{ succes }}</div>
      <div v-if="erreur" class="erreur">{{ erreur }}</div>

      <form v-if="!succes" @submit.prevent="envoyer">
        <div class="champ">
          <label>Email</label>
          <input type="email" v-model="email" required placeholder="votre@email.com" />
        </div>
        <button type="submit" :disabled="chargement">
          {{ chargement ? 'Envoi...' : 'Envoyer le lien' }}
        </button>
      </form>

      <p class="lien">
        <RouterLink to="/login">Retour à la connexion</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const email = ref('')
const succes = ref('')
const erreur = ref('')
const chargement = ref(false)

async function envoyer() {
  erreur.value = ''
  succes.value = ''
  chargement.value = true
  try {
    await api.post('/auth/mot-de-passe-oublie', { email: email.value })
    succes.value = 'Si cet email existe, un lien de réinitialisation vous a été envoyé.'
  } catch (e) {
    erreur.value = "Erreur lors de l'envoi."
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
  margin-bottom: 1rem;
  text-align: center;
}
.texte {
  color: #666;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 1.5rem;
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
