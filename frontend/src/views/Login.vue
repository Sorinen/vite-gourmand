<template>
<div class="login-page">
    <div class="login-card">
        <h1>Connexion</h1>
        <div v-if="erreur" class="erreur">{{ erreur }}</div>

        <form @submit.prevent="login">
            <div class="champ">
                <label>Email</label>
                <input type="email" v-model="email" required placeholder="votre@email.com" />
            </div>
            <div class="champ">
                <label>Mot de passe</label>
                <div class="input-password">
                    <input :type="showPassword ? 'text' : 'password'" v-model="motDePasse" required placeholder="••••••••" />
                    <button type="button" @click="showPassword = !showPassword">
                        {{ showPassword ? '🔓' : '🔒' }}
                    </button>
                </div>
            </div>
            <button type="submit" :disabled="chargement">
                {{ chargement ? 'Connexion...' : 'Se connecter' }}
            </button>
        </form>

        <p class="lien">
            Pas encore de compte ?
            <RouterLink to="/register">S'inscrire</RouterLink>
        </p>
    </div>
</div>
</template>

<script setup>
import {
    ref
} from 'vue'
import {
    useRouter
} from 'vue-router'
import {
    useAuthStore
} from '../stores/auth'
import api from '../services/api'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const motDePasse = ref('')
const erreur = ref('')
const chargement = ref(false)
const showPassword = ref(false)
async function login() {
    erreur.value = ''
    chargement.value = true
    try {
        const formData = new FormData()
        formData.append('username', email.value)
        formData.append('password', motDePasse.value)
        const res = await api.post('/auth/login', formData)
        authStore.setToken(res.data.access_token)
        const userRes = await api.get('/utilisateurs/')
        const user = userRes.data.find(u => u.email === email.value)
        authStore.setUser(user)
        if (authStore.isAdmin) {
            router.push('/admin')
        } else if (authStore.isEmploye) {
            router.push('/employe')
        } else {
            router.push('/')
        }
    } catch (e) {
        erreur.value = 'Email ou mot de passe incorrect'
    } finally {
        chargement.value = false
    }
}
</script>

<style scoped>
.login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    padding: 2rem;
}

.login-card {
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

.lien {
    text-align: center;
    margin-top: 1rem;
    color: #666;
}

.lien a {
    color: #1D9E75;
}

.input-password button {
    width: auto;
    padding: 0.5rem;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
}

.input-password {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}
</style>
