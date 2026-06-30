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

        <div class="conditions-box" v-if="menuSelectionne && menuSelectionne.conditions">
          <strong>⚠️ Conditions de ce menu :</strong>
          <p>{{ menuSelectionne.conditions }}</p>
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
          <label>Livraison</label>
          <div class="livraison-choix">
            <button type="button" :class="['btn-livraison', { actif: livraisonBordeaux }]" @click="livraisonBordeaux = true">
              📍 Bordeaux — Gratuit
            </button>
            <button type="button" :class="['btn-livraison', { actif: !livraisonBordeaux }]" @click="livraisonBordeaux = false">
              🚚 Hors Bordeaux — +15€
            </button>
          </div>
          <input
            v-if="!livraisonBordeaux"
            type="text"
            v-model="ville"
            required
            placeholder="Nom de votre ville"
            class="input-ville"
          />
          <p v-else class="ville-bordeaux">Bordeaux</p>
        </div>

        <div class="champ">
          <label>Nombre de personnes</label>
          <input type="number" v-model="nombrePersonnes" required :min="menuSelectionne ? menuSelectionne.nombre_personnes_min : 1" />
          <p v-if="menuSelectionne && nombrePersonnes < menuSelectionne.nombre_personnes_min" class="alerte-min">
            Minimum {{ menuSelectionne.nombre_personnes_min }} personnes pour ce menu.
          </p>
          <p v-if="reductionActive" class="alerte-reduction">
            🎉 Réduction de 10% appliquée (commande de {{ menuSelectionne.nombre_personnes_min + 5 }} personnes ou plus) !
          </p>
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
            Louer le matériel (tables, chaises) — +15€
          </label>
        </div>

        <div class="resume" v-if="menuSelectionne">
          <h3>Résumé</h3>
          <p>Menu : {{ menuSelectionne.titre }}</p>
          <p>Prix par personne : {{ menuSelectionne.prix_base }}€</p>
          <p>Nombre de personnes : {{ nombrePersonnes }}</p>
          <p>Sous-total menu : {{ sousTotal }}€</p>
          <p v-if="reductionActive" class="reduction">Réduction 10% : -{{ montantReduction }}€</p>
          <p v-if="pretMateriel" class="supplement">Location matériel : +15€</p>
          <p v-else class="inclus">Sans location matériel : 0€</p>
          <p v-if="!livraisonBordeaux" class="supplement">Livraison hors Bordeaux : +15€</p>
          <p v-else class="inclus">Livraison Bordeaux : Gratuit</p>
          <p class="total">Total : {{ prixTotal }}€</p>
        </div>

        <button type="submit" :disabled="chargement || commandeInvalide">
          {{ chargement ? 'Envoi...' : 'Confirmer la commande' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
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
const livraisonBordeaux = ref(true)
const nombrePersonnes = ref(1)
const modeContact = ref('email')
const pretMateriel = ref(false)
const erreur = ref('')
const succes = ref('')
const chargement = ref(false)

const menuSelectionne = computed(() => {
  return menus.value.find(m => m.id === Number(menuId.value))
})

const reductionActive = computed(() => {
  if (!menuSelectionne.value) return false
  return Number(nombrePersonnes.value) >= menuSelectionne.value.nombre_personnes_min + 5
})

const sousTotal = computed(() => {
  if (!menuSelectionne.value) return 0
  return menuSelectionne.value.prix_base * Number(nombrePersonnes.value)
})

const montantReduction = computed(() => {
  if (!reductionActive.value) return 0
  return Math.round(sousTotal.value * 0.1 * 100) / 100
})

const prixLivraison = computed(() => {
  return livraisonBordeaux.value ? 0 : 15
})

const prixLocation = computed(() => {
  return pretMateriel.value ? 15 : 0
})

const prixTotal = computed(() => {
  if (!menuSelectionne.value) return 0
  return Math.round((sousTotal.value - montantReduction.value + prixLivraison.value + prixLocation.value) * 100) / 100
})

const commandeInvalide = computed(() => {
  if (!menuSelectionne.value) return true
  return Number(nombrePersonnes.value) < menuSelectionne.value.nombre_personnes_min
})

const villeFinale = computed(() => {
  return livraisonBordeaux.value ? 'Bordeaux' : ville.value
})

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  try {
    const res = await api.get('/menu/')
    menus.value = res.data
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

  if (Number(nombrePersonnes.value) < menuSelectionne.value.nombre_personnes_min) {
    erreur.value = `Le nombre minimum de personnes pour ce menu est ${menuSelectionne.value.nombre_personnes_min}.`
    chargement.value = false
    return
  }

  if (!livraisonBordeaux.value && !ville.value.trim()) {
    erreur.value = 'Veuillez saisir votre ville.'
    chargement.value = false
    return
  }

  try {
    await api.post('/commandes/', {
      date_prestation: datePrestation.value,
      heure_livraison: heureLivraison.value,
      adresse_livraison: adresseLivraison.value + ', ' + villeFinale.value,
      nombre_personnes: Number(nombrePersonnes.value),
      prix_menu: sousTotal.value - montantReduction.value,
      prix_livraison: prixLivraison.value + prixLocation.value,
      prix_total: prixTotal.value,
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

.conditions-box {
  background: #fff8e6;
  border: 1px solid #f5d77a;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  color: #5f3a08;
  font-size: 0.9rem;
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

.alerte-min {
  color: #c0392b;
  font-size: 0.85rem;
  margin-top: 0.4rem;
}

.alerte-reduction {
  color: #1D9E75;
  font-size: 0.85rem;
  margin-top: 0.4rem;
  font-weight: bold;
}

.checkbox input {
  width: auto;
  margin-right: 0.5rem;
}

.livraison-choix {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.btn-livraison {
  flex: 1;
  padding: 0.7rem;
  border: 2px solid #ccc;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.btn-livraison.actif {
  border-color: #1D9E75;
  background: #f0f9f5;
  color: #085041;
  font-weight: bold;
}

.input-ville {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  margin-top: 0.5rem;
}

.ville-bordeaux {
  color: #1D9E75;
  font-weight: bold;
  padding: 0.3rem 0;
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

.supplement {
  color: #e67e22;
  font-weight: bold;
}

.reduction {
  color: #1D9E75;
  font-weight: bold;
}

.inclus {
  color: #1D9E75;
}

.total {
  font-weight: bold;
  color: #085041;
  margin-top: 0.5rem;
  font-size: 1.2rem;
  border-top: 2px solid #1D9E75;
  padding-top: 0.5rem;
}

button[type="submit"] {
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

button[type="submit"]:disabled {
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
  .commande-page { padding: 1rem; }
  .livraison-choix { flex-direction: column; }
}
</style>
