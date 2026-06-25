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
</style>
