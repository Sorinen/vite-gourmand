<template>
    <div>

        <!-- HERO -->
        <section class="hero">
            <div class="hero-content">
                <span class="badge">Depuis 25 ans à Bordeaux</span>

                <h1>Vite & Gourmand</h1>

                <p class="subtitle">
                    Julie et José vous accompagnent dans tous vos événements avec des menus
                    savoureux, préparés avec passion et renouvelés tout au long de l'année.
                </p>

                <p class="description">
                    Noël, Pâques, anniversaires, repas de famille ou événements
                    professionnels, découvrez des prestations de qualité adaptées à toutes
                    les occasions.
                </p>

                <div class="hero-buttons">
                    <RouterLink to="/menus" class="btn-primary">
                        Découvrir nos menus
                    </RouterLink>

                    <RouterLink to="/contact" class="btn-secondary">
                        Nous contacter
                    </RouterLink>
                </div>
            </div>
        </section>

        <!-- PRESENTATION -->
        <section class="about">
            <div class="container">
                <h2>Une histoire de passion culinaire</h2>

                <p>
                    Créée par Julie et José, Vite & Gourmand accompagne les particuliers
                    et les professionnels depuis plus de 25 ans.
                </p>

                <p>
                    Grâce à leur expérience, ils élaborent des menus variés et évolutifs
                    afin de proposer à leurs clients des plats adaptés aux saisons et aux
                    événements de l'année.
                </p>

                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>25+</h3>
                        <p>Années d'expérience</p>
                    </div>

                    <div class="stat-card">
                        <h3>100%</h3>
                        <p>Passion & savoir-faire</p>
                    </div>

                    <div class="stat-card">
                        <h3>Toute l'année</h3>
                        <p>Menus renouvelés</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- AVANTAGES -->
        <section class="advantages">
            <div class="container">
                <h2>Pourquoi choisir Vite & Gourmand ?</h2>

                <div class="advantages-grid">
                    <div class="advantage-card">
                        <div class="icon">🍽️</div>
                        <h3>Menus variés</h3>
                        <p>
                            Des menus régulièrement renouvelés pour satisfaire tous les goûts.
                        </p>
                    </div>

                    <div class="advantage-card">
                        <div class="icon">🎉</div>
                        <h3>Tous vos événements</h3>
                        <p>
                            Mariages, anniversaires, fêtes de famille ou événements d'entreprise.
                        </p>
                    </div>

                    <div class="advantage-card">
                        <div class="icon">⭐</div>
                        <h3>25 ans d'expérience</h3>
                        <p>
                            Une expertise reconnue dans la préparation de repas événementiels.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- MENUS -->
        <section class="featured">
            <div class="container">
                <h2>Nos menus en vedette</h2>

                <div class="menus-grid" v-if="menus.length">
                    <div
                        class="menu-card"
                        v-for="menu in menus.slice(0, 3)"
                        :key="menu.id"
                    >
                        <h3>{{ menu.titre }}</h3>

                        <p>{{ menu.description }}</p>

                        <div class="prix">
                            À partir de {{ menu.prix_base }} € / personne
                        </div>

                        <RouterLink
                            :to="`/menu/${menu.id}`"
                            class="btn-card"
                        >
                            Voir le menu
                        </RouterLink>
                    </div>
                </div>

                <div v-else class="empty">
                    Aucun menu disponible pour le moment.
                </div>
            </div>
        </section>

        <!-- HORAIRES -->
        <section class="horaires">
            <div class="container">
                <h2>Nos horaires</h2>

                <div class="horaire-card">
                    <div class="horaire-row">
                        <span>Lundi - Vendredi</span>
                        <span>08h00 - 18h00</span>
                    </div>

                    <div class="horaire-row">
                        <span>Samedi</span>
                        <span>08h00 - 16h00</span>
                    </div>

                    <div class="horaire-row">
                        <span>Dimanche</span>
                        <span class="closed">Fermé</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA -->
        <section class="cta">
            <div class="container">
                <h2>Organisez votre prochain événement avec nous</h2>

                <p>
                    Découvrez nos menus et trouvez la formule idéale pour vos invités.
                </p>

                <RouterLink to="/menus" class="btn-card">
                    Voir le menu
                </RouterLink>
            </div>
        </section>

    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const menus = ref([])

onMounted(async () => {
    try {
        const response = await api.get("/menu/")
        menus.value = response.data
    } catch (error) {
        console.error("Erreur chargement menus :", error)
    }
})
</script>

<style scoped>
* {
    box-sizing: border-box;
}

.container {
    max-width: 1200px;
    margin: auto;
    padding: 0 20px;
}

/* HERO */

.hero {
    min-height: 80vh;
    background:
        linear-gradient(rgba(0,0,0,.55), rgba(0,0,0,.55)),
        url("https://images.unsplash.com/photo-1555244162-803834f70033");
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
}

.hero-content {
    max-width: 800px;
    padding: 20px;
}

.badge {
    background: rgba(255,255,255,.2);
    padding: 8px 18px;
    border-radius: 30px;
    display: inline-block;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 4rem;
    margin-bottom: 20px;
}

.subtitle {
    font-size: 1.4rem;
    margin-bottom: 20px;
    line-height: 1.7;
}

.description {
    line-height: 1.8;
    margin-bottom: 30px;
}

.hero-buttons {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
}

.btn-primary,
.btn-secondary,
.btn-card,
.btn-light {
    text-decoration: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    transition: .3s;
}

.btn-primary {
    background: #1D9E75;
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
}

.btn-secondary {
    border: 2px solid white;
    color: white;
}

.btn-light {
    background: white;
    color: #1D9E75;
}


.about {
    padding: 80px 0;
}

.about h2 {
    text-align: center;
    color: #1D9E75;
    margin-bottom: 30px;
}

.about p {
    text-align: center;
    max-width: 800px;
    margin: auto auto 20px;
    line-height: 1.8;
}

.stats-grid {
    margin-top: 50px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px,1fr));
    gap: 20px;
}

.stat-card {
    background: white;
    padding: 30px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,.08);
}

.stat-card h3 {
    font-size: 2.2rem;
    color: #1D9E75;
}

.advantages {
    background: #f8f8f8;
    padding: 80px 0;
}

.advantages h2 {
    text-align: center;
    color: #1D9E75;
    margin-bottom: 50px;
}

.advantages-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px,1fr));
    gap: 25px;
}

.advantage-card {
    background: white;
    padding: 30px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,.08);
}

.icon {
    font-size: 3rem;
    margin-bottom: 15px;
}

.featured {
    padding: 80px 0;
}

.featured h2 {
    text-align: center;
    color: #1D9E75;
    margin-bottom: 50px;
}

.menus-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px,1fr));
    gap: 25px;
}

.menu-card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,.08);
}

.menu-card h3 {
    color: #1D9E75;
    margin-bottom: 15px;
}

.prix {
    margin: 20px 0;
    font-weight: bold;
    color: #444;
}

.btn-card {
    display: inline-block;
    background: #1D9E75;
    color: white;
}

.empty {
    text-align: center;
}

.horaires {
    background: #f4ead8;
    padding: 80px 0;
}

.horaires h2 {
    text-align: center;
    color: #1D9E75;
    margin-bottom: 40px;
}

.horaire-card {
    background: white;
    max-width: 700px;
    margin: auto;
    border-radius: 12px;
    padding: 20px;
}

.horaire-row {
    display: flex;
    justify-content: space-between;
    padding: 15px;
    border-bottom: 1px solid #eee;
}

.horaire-row:last-child {
    border-bottom: none;
}

.closed {
    color: red;
    font-weight: bold;
}


.cta {
    background: #1D9E75;
    color: white;
    text-align: center;
    padding: 80px 20px;
}

.cta h2 {
    margin-bottom: 20px;
}

.cta p {
    margin-bottom: 30px;
}

</style>