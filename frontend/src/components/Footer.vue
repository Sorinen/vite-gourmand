<template>
<footer class="footer">
    <div class="footer-content">
        <div class="footer-section">
            <h3>Vite & Gourmand</h3>
            <p>Traiteur événementiel à Bordeaux</p>
            <p>📍 Bordeaux, France</p>
            <p>📞 05 56 12 34 56</p>
            <p>✉️ contact@zotpresta.re</p>
        </div>
        <div class="footer-section">
            <h3>Horaires</h3>
            <p>Lundi — Vendredi : 08h00 - 18h00</p>
            <p>Samedi : 08h00 - 16h00</p>
            <p>Dimanche : Fermé</p>
        </div>
        <div class="footer-section">
            <h3>Navigation</h3>
            <RouterLink to="/">Accueil</RouterLink>
            <RouterLink to="/menus">Nos Menus</RouterLink>
            <RouterLink to="/contact">Contact</RouterLink>
        </div>
        <div class="footer-section">
            <h3>Informations légales</h3>
            <RouterLink to="/mentions-legales">Mentions légales</RouterLink>
            <RouterLink to="/cgv">Conditions générales de vente</RouterLink>
        </div>
    </div>
    <div class="footer-bottom">
        <p>© 2026 Vite & Gourmand — Tous droits réservés</p>
    </div>
</footer>
</template>

<script setup>
</script>

<style>
.footer {
    background-color: #085041;
    color: white;
    margin-top: auto;
}

.footer-content {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    padding: 3rem 2rem 1rem 2rem;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.footer-section h3 {
    color: #1D9E75;
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.footer-section p {
    margin-bottom: 0.5rem;
    color: #ccc;
    font-size: 0.9rem;
}

.footer-section a {
    display: block;
    color: #ccc;
    text-decoration: none;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.footer-section a:hover {
    color: #1D9E75;
}

.footer-bottom {
    text-align: center;
    padding: 0.5rem 1rem;
    color: #ccc;
    font-size: 0.85rem;
}

@media (max-width: 768px) {
    .footer-content {
        flex-direction: column;
        text-align: center;
        padding: 2rem 1rem 1rem;
    }
}
</style>
