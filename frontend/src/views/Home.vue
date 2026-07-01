<template>
<div>
    <section class="hero">
        <div class="hero-content">
            <h1>Vite & Gourmand</h1>
            <span class="badge">
                Depuis 25 ans à Bordeaux
            </span>
            <p class="subtitle">
                Julie et José vous accompagnent dans tous vos événements avec des
                menus savoureux, préparés avec passion et renouvelés tout au long
                de l'année.
            </p>
            <p class="description">
                Noël, Pâques, anniversaires, repas de famille ou événements
                professionnels, découvrez des prestations adaptées à toutes les
                occasions.
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
    <section class="about">
        <div class="container">
            <h2>Une histoire de passion culinaire</h2>
            <p>
                Créée par Julie et José, Vite & Gourmand accompagne les particuliers
                et les professionnels depuis plus de vingt-cinq ans.
            </p>
            <p>
                Grâce à leur expérience, ils élaborent des menus variés afin de
                proposer des prestations adaptées à chaque saison et à chaque
                événement.
            </p>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>25+</h3>
                    <p>Années d'expérience</p>
                </div>
                <div class="stat-card">
                    <h3>100%</h3>
                    <p>Produits sélectionnés avec soin</p>
                </div>
                <div class="stat-card">
                    <h3>Toute l'année</h3>
                    <p>Menus renouvelés</p>
                </div>
            </div>
        </div>
    </section>
    <section class="advantages">
        <div class="container">
            <h2>Pourquoi choisir Vite & Gourmand ?</h2>
            <div class="advantages-grid">
                <div class="advantage-card">
                    <div class="number">
                        01
                    </div>
                    <h3>Menus variés</h3>
                    <p>
                        Une carte évolutive afin de satisfaire toutes les envies.
                    </p>
                </div>
                <div class="advantage-card">
                    <div class="number">
                        02
                    </div>
                    <h3>Tous vos événements</h3>
                    <p>
                        Mariages, anniversaires, repas d'entreprise ou réceptions privées.
                    </p>
                </div>
                <div class="advantage-card">
                    <div class="number">
                        03
                    </div>
                    <h3>Une véritable expérience</h3>
                    <p>
                        Plus de vingt-cinq années de savoir-faire au service de vos invités.
                    </p>
                </div>
            </div>
        </div>
    </section>
    <section class="featured">
        <div class="container">
            <h2>Nos menus en vedette</h2>
            <div class="menus-grid" v-if="menus.length">
                <div class="menu-card" v-for="menu in menus.slice(0,3)" :key="menu.id">
                    <h3>{{ menu.titre }}</h3>
                    <p class="description-menu">
                        {{ menu.description }}
                    </p>
                    <div class="prix">
                        À partir de {{ menu.prix_base }} € / personne
                    </div>
                    <div class="avis-mini" v-if="getAvisMenu(menu.id).length">
                        <div class="avis-mini-item" v-for="a in getAvisMenu(menu.id).slice(0,2)" :key="a.id">
                            <span class="etoiles">
                                {{ '★'.repeat(a.note) }}{{ '☆'.repeat(5-a.note) }}
                            </span>
                            <span class="commentaire-mini">
                                {{ a.commentaire }}
                            </span>
                        </div>
                    </div>
                    <RouterLink to="/menus" class="btn-card">
                        Voir le menu
                    </RouterLink>
                </div>
            </div>
            <div class="empty" v-else>
                Aucun menu disponible pour le moment.
            </div>
        </div>
    </section>
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
    <section class="cta">
        <div class="container">
            <h2>
                Organisez votre prochain événement avec nous
            </h2>
            <p>
                Découvrez nos menus et trouvez la formule idéale pour vos invités.
            </p>
            <RouterLink to="/menus" class="btn-light">
                Voir tous les menus
            </RouterLink>
        </div>
    </section>
</div>
</template>

<script setup>
import {
    ref,
    onMounted
} from 'vue'
import api from '../services/api'

const menus = ref([])
const avis = ref([])

function getAvisMenu(menuId) {
    return avis.value.filter(
        a => a.statut === 'valide' && Number(a.menu_id) === Number(menuId)
    )
}

async function chargerDonnees() {
    try {
        const [menusRes, avisRes] = await Promise.all([
            api.get('/menu/'),
            api.get('/avis/')
        ])

        menus.value = menusRes.data
        avis.value = avisRes.data
    } catch (error) {
        console.error('Erreur lors du chargement des données :', error)
    }
}

onMounted(() => {
    chargerDonnees()
})
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: Inter, Segoe UI, sans-serif;
    background: #f7f8fa;
    color: #222;
}

.container {
    width: min(1200px, 92%);
    margin: auto;
}

.hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    overflow: hidden;
    background:
        linear-gradient(rgba(0, 0, 0, .55),
            rgba(0, 0, 0, .55)),
        url("https://static.wixstatic.com/media/d663dd_11bbaba2036148d48fdfe83eaddc6567~mv2.jpeg/v1/fill/w_2560,h_1440,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/d663dd_11bbaba2036148d48fdfe83eaddc6567~mv2.jpeg");
    background-size: cover;
    background-position: center;
}

.hero::after {

    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 120px;
    background: linear-gradient(transparent,
            #f7f8fa);
}

.hero-content {

    position: relative;
    z-index: 5;
    max-width: 900px;
    padding: 20px;
}

.badge {

    display: inline-block;
    padding: 10px 22px;
    border-radius: 50px;
    background: rgba(255, 255, 255, .12);
    border: 1px solid rgba(255, 255, 255, .25);
    backdrop-filter: blur(12px);
    color: white;
    letter-spacing: .5px;
    margin-bottom: 35px;
}

.hero h1 {
    color: white;
    font-size: clamp(4rem, 8vw, 7rem);
    line-height: 1;
    font-weight: 800;
    margin-bottom: 30px;
    text-shadow:
        0 8px 25px rgba(0, 0, 0, .35);
}

.subtitle {
    color: #f2f2f2;
    font-size: 1.35rem;
    line-height: 1.8;
    margin: auto;
    max-width: 760px;
    margin-bottom: 25px;
}

.description {
    color: #dddddd;
    line-height: 1.9;
    font-size: 1.05rem;
    max-width: 700px;
    margin: auto;
    margin-bottom: 45px;
}

.hero-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.btn-primary,
.btn-secondary,
.btn-card,
.btn-light {
    padding: 15px 34px;
    border-radius: 12px;
    text-decoration: none;
    transition: .30s;
    font-weight: 600;
    display: inline-block;
}

.btn-primary {
    background: #1D9E75;
    color: white;
    box-shadow:
        0 15px 35px rgba(29, 158, 117, .35);
}

.btn-primary:hover {
    transform: translateY(-5px);
    background: #168260;
}

.btn-secondary {
    color: white;
    border: 2px solid rgba(255, 255, 255, .75);
}

.btn-secondary:hover {
    background: white;
    color: #1D9E75;
}

section {
    padding: 110px 0;
}

h2 {
    font-size: 2.8rem;
    color: #1D9E75;
    text-align: center;
    margin-bottom: 18px;
    font-weight: 700;
}

h2::after {
    content: "";
    display: block;
    width: 70px;
    height: 4px;
    background: #1D9E75;
    margin: 18px auto 0;
    border-radius: 5px;
}

.about p {
    text-align: center;
    max-width: 850px;
    margin: 18px auto;
    color: #555;
    line-height: 1.9;
    font-size: 1.05rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    margin-top: 60px;
}

.stat-card {
    background: white;
    border-radius: 20px;
    padding: 45px 30px;
    text-align: center;
    transition: .35s;
    box-shadow: 0 15px 35px rgba(0, 0, 0, .06);
}

.stat-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 25px 55px rgba(0, 0, 0, .12);
}

.stat-card h3 {
    font-size: 3rem;
    color: #1D9E75;
    margin-bottom: 15px;
}

.stat-card p {
    margin: 0;
    color: #666;
}

.advantages {
    background: #f2f5f6;
}

.advantages-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 60px;
}

.advantage-card {
    background: white;
    border-radius: 20px;
    padding: 45px 35px;
    text-align: center;
    transition: .35s;
    box-shadow: 0 15px 35px rgba(0, 0, 0, .06);
}

.advantage-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 25px 55px rgba(0, 0, 0, .12);
}

.number {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: #1D9E75;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 700;
    font-size: 1.3rem;
    margin: auto auto 25px;
}

.advantage-card h3 {
    margin-bottom: 18px;
    color: #1D9E75;
    font-size: 1.4rem;
}

.advantage-card p {
    color: #666;
    line-height: 1.8;
}

.featured {
    background: white;
}

.menus-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin-top: 60px;
}

.menu-card {
    background: white;
    border-radius: 22px;
    overflow: hidden;
    position: relative;
    padding: 35px;
    display: flex;
    flex-direction: column;
    transition: .35s;
    box-shadow: 0 15px 35px rgba(0, 0, 0, .06);
}

.menu-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 6px;
    background: #1D9E75;
}

.menu-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 30px 60px rgba(0, 0, 0, .12);
}

.menu-card h3 {
    color: #1D9E75;
    font-size: 1.5rem;
    margin-bottom: 20px;
}

.description-menu {
    flex: 1;
    color: #666;
    line-height: 1.8;
}

.prix {
    margin: 25px 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: #222;
}

.btn-card {
    background: #1D9E75;
    color: white;
    text-align: center;
    margin-top: auto;
}

.btn-card:hover {
    background: #168260;
    transform: translateY(-3px);
}

.avis-mini {
    margin: 20px 0;
    border-top: 1px solid #ececec;
    padding-top: 20px;
}

.avis-mini-item {
    margin-bottom: 15px;
}

.etoiles {
    color: #f3b200;
    display: block;
    margin-bottom: 5px;
}

.commentaire-mini {
    color: #777;
    font-size: .95rem;
    font-style: italic;
}

.empty {
    text-align: center;
    color: #777;
    font-size: 1.1rem;
    margin-top: 40px;
}

.horaires {
    background: #f8f9fa;
}

.horaire-card {
    max-width: 720px;
    margin: 60px auto 0;
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0, 0, 0, .06);
}

.horaire-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 22px 30px;
    border-bottom: 1px solid #ececec;
    transition: .3s;
}

.horaire-row:last-child {
    border-bottom: none;
}

.horaire-row:hover {
    background: #fafafa;
}

.horaire-row span:first-child {
    font-weight: 600;
    color: #333;
}

.horaire-row span:last-child {
    color: #666;
}

.closed {
    color: #d63c3c !important;
    font-weight: 700;
}

.cta {
    background: linear-gradient(135deg,
            #1D9E75,
            #15765b);
    color: white;
    text-align: center;
    padding: 120px 20px;
}

.cta h2 {
    color: white;
    margin-bottom: 25px;
}

.cta h2::after {
    background: white;
}

.cta p {
    max-width: 700px;
    margin: 0 auto 40px;
    line-height: 1.9;
    color: rgba(255, 255, 255, .9);
}

.btn-light {
    background: white;
    color: #1D9E75;
    box-shadow: 0 15px 35px rgba(0, 0, 0, .18);
}

.btn-light:hover {
    transform: translateY(-5px);
}

.stat-card,
.menu-card,
.advantage-card,
.btn-primary,
.btn-secondary,
.btn-light {
    transition:
        transform .3s,
        box-shadow .3s,
        background .3s;
}


@media (max-width:1100px) {
    .menus-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width:768px) {
    .hero {
        min-height: 90vh;
        padding: 40px 0;
    }
    .hero h1 {
        font-size: 3rem;
    }
    .subtitle {
        font-size: 1.1rem;
    }
    .description {
        font-size: 1rem;
    }
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    .btn-primary,
    .btn-secondary,
    .btn-light {
        width: 100%;
        max-width: 320px;
    }
    .menus-grid {
        grid-template-columns: 1fr;
    }
    .stats-grid {
        grid-template-columns: 1fr;
    }
    .advantages-grid {
        grid-template-columns: 1fr;
    }
    .horaire-row {
        flex-direction: column;
        gap: 8px;
        text-align: center;
    }
    h2 {
        font-size: 2.1rem;
    }
    section {
        padding: 80px 0;
    }
}

@media (max-width:480px) {
    .hero h1 {
        font-size: 2.4rem;
    }
    .badge {
        font-size: .9rem;
    }
    .subtitle {
        font-size: 1rem;
    }
    .container {
        width: 94%;
    }
    .menu-card,
    .stat-card,
    .advantage-card {
        padding: 25px;
    }
}
</style>
