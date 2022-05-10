<script setup>
</script>

<template>
    <main>
        <h1>Public page for UNAUTHENTICATED users.</h1>
        <router-link 
            :to="{name: 'home'}" 
            event=""
        >
            <button>Login</button>
        </router-link> 
    </main>
</template>
