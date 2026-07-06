<template>
<div class="contact-page">
    <div class="contact-card">
        <h1>Contactez-nous</h1>

        <div v-if="succes" class="succes">{{ succes }}</div>
        <div v-if="erreur" class="erreur">{{ erreur }}</div>

        <form @submit.prevent="envoyer">
            <div class="champ">
                <label>Nom</label>
                <input type="text" v-model="nom" required placeholder="Votre nom" />
            </div>
            <div class="champ">
                <label>Email</label>
                <input type="email" v-model="email" required placeholder="votre@email.com" />
            </div>
            <div class="champ">
                <label>Téléphone</label>
                <input type="text" v-model="telephone" placeholder="06 92 12 34 56" />
            </div>
            <div class="champ">
                <label>Message</label>
                <textarea v-model="message" required placeholder="Votre message..." rows="5"></textarea>
            </div>
            <button type="submit" :disabled="chargement">
                {{ chargement ? "Envoi..." : "Envoyer" }}
            </button>
        </form>
    </div>
</div>
</template>

<script setup>
import {
    ref
} from "vue";
import api from "../services/api";

const nom = ref("");
const email = ref("");
const telephone = ref("");
const message = ref("");
const succes = ref("");
const erreur = ref("");
const chargement = ref(false);

async function envoyer() {
    erreur.value = "";
    succes.value = "";
    chargement.value = true;

    try {
        await api.post("/contact/", {
            nom: nom.value,
            email: email.value,
            telephone: telephone.value,
            message: message.value,
        });
        succes.value = "Votre message a bien été envoyé !";
        nom.value = "";
        email.value = "";
        telephone.value = "";
        message.value = "";
    } catch (e) {
        erreur.value = "Erreur lors de l'envoi du message.";
    } finally {
        chargement.value = false;
    }
}
</script>

<style scoped>
.contact-page {
    display: flex;
    justify-content: center;
    padding: 3rem 2rem;
}

.contact-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 500px;
}

h1 {
    color: #1d9e75;
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

.champ input,
.champ textarea {
    width: 100%;
    padding: 0.7rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    font-family: inherit;
}

button {
    width: 100%;
    padding: 0.8rem;
    background: #1d9e75;
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
