<template>
    <div class="register-page">
        <div class="register-card">
            <h1>Inscription</h1>

            <div v-if="erreur" class="erreur">{{ erreur }}</div>
            <div v-if="succes" class="succes">{{ succes }}</div>

            <form @submit.prevent="register">
                <div class="champ">
                    <label>Prénom*</label>
                    <input v-model="prenom" type="text" required placeholder="Votre prénom" />
                </div>

                <div class="champ">
                    <label>Nom*</label>
                    <input v-model="nom" type="text" required placeholder="Votre nom" />
                </div>

                <div class="champ">
                    <label>Email*</label>
                    <input v-model="email" type="email" required placeholder="votre@email.com" />
                </div>

                <div class="champ">
                    <label>Téléphone</label>
                    <input v-model="telephone" type="text" placeholder="0692000000" />
                </div>

                <div class="champ">
                    <label>Mot de passe*</label>
                    <div class="input-password">
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            v-model="motDePasse"
                            required
                            placeholder="••••••••"
                        />
                        <button type="button" @click="showPassword = !showPassword">
                            {{ showPassword ? '🔓' : '🔒' }}
                        </button>
                    </div>
                </div>

                <div class="champ">
                    <label>Confirmer le mot de passe*</label>
                    <div class="input-password">
                        <input
                            :type="showConfirm ? 'text' : 'password'"
                            v-model="confirmerMotDePasse"
                            required
                            placeholder="••••••••"
                        />
                        <button type="button" @click="showConfirm = !showConfirm">
                            {{ showConfirm ? '🔓' : '🔒' }}
                        </button>
                    </div>
                </div>

                <button type="submit" :disabled="chargement">
                    {{ chargement ? 'Inscription...' : "S'inscrire" }}
                </button>
            </form>

            <p class="lien">
                Déjà un compte ?
                <RouterLink to="/login">Se connecter</RouterLink>
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const prenom = ref('')
const nom = ref('')
const email = ref('')
const telephone = ref('')
const motDePasse = ref('')
const confirmerMotDePasse = ref('')

const erreur = ref('')
const succes = ref('')
const chargement = ref(false)

const showPassword = ref(false)
const showConfirm = ref(false)

async function register() {
    erreur.value = ''
    succes.value = ''
    chargement.value = true

    if (motDePasse.value !== confirmerMotDePasse.value) {
        erreur.value = 'Les mots de passe ne correspondent pas.'
        chargement.value = false
        return
    }

    try {
        await api.post('/utilisateurs/', {
            prenom: prenom.value,
            nom: nom.value,
            email: email.value,
            telephone: telephone.value,
            mot_de_passe: motDePasse.value,
            role_id: 3
        })

        succes.value = 'Compte créé avec succès ! Vous pouvez vous connecter.'

        setTimeout(() => {
            router.push('/login')
        }, 2000)

    } catch (e) {
        if (e.response?.data?.detail === 'Email déjà utilisé') {
            erreur.value = 'Cet email est déjà utilisé.'
        } else {
            erreur.value = "Erreur lors de l'inscription."
        }
    } finally {
        chargement.value = false
    }
}
</script>

<style scoped>
.register-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    padding: 2rem;
}

.register-card {
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
    color: #666;
}

.lien a {
    color: #1D9E75;
}

.input-password {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.input-password button {
    width: auto;
    padding: 0.5rem;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
}
</style>