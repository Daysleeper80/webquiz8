<script setup>
import { RouterView } from "vue-router";

</script>

<template>
    <main>
        <header>
            Header stuff common to all views...
        </header>

        <router-view />

        <footer>
            Links and legalese common to all views...
        </footer>
    </main>
</template>

<style>
@import "@/assets/styles/base.css";

#app {
    margin: 1em;
}

footer {
    position: fixed;
    bottom: 0;
}
</style>
