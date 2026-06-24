<template>
<div class="mes-commandes-page">
    <h1>Mes commandes</h1>

    <div v-if="commandes.length > 0">
        <div class="commande-card" v-for="commande in commandes" :key="commande.id">
            <div class="commande-header">
                <span class="commande-id">#{{ commande.id }}</span>
                <span :class="['statut', commande.statut]">{{ commande.statut }}</span>
            </div>
            <p><strong>Date :</strong> {{ commande.date_prestation }}</p>
            <p><strong>Adresse :</strong> {{ commande.adresse_livraison }}</p>
            <p><strong>Personnes :</strong> {{ commande.nombre_personnes }}</p>
            <p><strong>Total :</strong> {{ commande.prix_total }}€</p>
        </div>
    </div>
    <p v-else>Vous n'avez pas encore de commande.</p>
</div>
</template>

<script setup>
import {
    ref,
    onMounted
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
const commandes = ref([])

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
})
</script>

<style scoped>
.mes-commandes-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

h1 {
    color: #1D9E75;
    margin-bottom: 2rem;
    text-align: center;
}

.commande-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
}

.commande-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.commande-id {
    font-weight: bold;
    font-size: 1.1rem;
    color: #1D9E75;
}

.statut {
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: bold;
}

.en_attente {
    background: #fff3cd;
    color: #856404;
}

.confirmee {
    background: #d4edda;
    color: #155724;
}

.annulee {
    background: #f8d7da;
    color: #721c24;
}

.terminee {
    background: #cce5ff;
    color: #004085;
}
</style>
