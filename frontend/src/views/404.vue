<template>
<div class="not-found">
    <h1>404</h1>
    <p>Oups, cette page n'existe pas.</p>
    <RouterLink to="/" class="btn">Retour à l'accueil</RouterLink>
</div>
</template>

<script setup>
</script>

<style scoped>
.not-found {
    text-align: center;
    padding: 5rem 2rem;
}

h1 {
    font-size: 6rem;
    color: #1D9E75;
    margin-bottom: 1rem;
}

p {
    font-size: 1.3rem;
    color: #666;
    margin-bottom: 2rem;
}

.btn {
    background: #1D9E75;
    color: white;
    padding: 0.8rem 2rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: bold;
}
</style>
