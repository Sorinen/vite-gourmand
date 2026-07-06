<template>
<div id="app">
    <NavBar />
    <RouterView />
    <Footer />
</div>
</template>

<script setup>
import NavBar from "./components/NavBar.vue";
import Footer from "./components/Footer.vue";
</script>

<style >
#app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: inherit;
}

#app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

@media (max-width: 768px) {
    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.2rem; }
}

</style>
