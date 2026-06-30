<template>
  <div class="page-legale">
    <h1>Mentions légales</h1>
    <section>
      <h2>Éditeur du site</h2>
      <p>Vite & Gourmand<br/>
      Julie et José<br/>
      Bordeaux, France<br/>
      Email : contact@zotpresta.re</p>
    </section>
    <section>
      <h2>Hébergement</h2>
      <p>Le site est hébergé par Hostinger.</p>
    </section>
    <section>
      <h2>Propriété intellectuelle</h2>
      <p>L'ensemble du contenu de ce site (textes, images, logo) est la propriété de Vite & Gourmand, sauf mention contraire. Toute reproduction sans autorisation est interdite.</p>
    </section>
    <section>
      <h2>Données personnelles</h2>
      <p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification et de suppression de vos données personnelles. Pour exercer ce droit, contactez-nous via le formulaire de contact.</p>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page-legale {
  max-width: 800px;
  margin: 0 auto;
  padding: 3rem 2rem;
}
h1 {
  color: #1D9E75;
  margin-bottom: 2rem;
  text-align: center;
}
h2 {
  color: #085041;
  margin: 1.5rem 0 0.5rem;
}
p {
  line-height: 1.7;
  color: #444;
}
@media (max-width: 768px) {
  .page-legale { padding: 1.5rem 1rem; }
}
</style>
