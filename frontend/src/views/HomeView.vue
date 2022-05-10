<script setup>
import { reactive } from 'vue';
import { sessionManager } from '@/assets/scripts/user-management';

// Apesar do ES2022 aceitar await no top-level, o seguinte ainda não 
// funciona com Vue 3:
//
//      let currUser = await sessionManager.getUser();
//
// Como o objecto 'currUser'vai ser actualizado após ter sido declarado
// (pq. a função getUser é assíncrona), temos que o declarar o objecto
// 'currUser' como 'reactive' para que a Vue acompanhe as alterações 
// dos valores das propriedades. Pelos motivos em cima indicados, 
// não podemos actualizar o objecto desta forma.
//
//      let currUser = reactive({username: '', email: ''});
//      Object.assign(currUser, await sessionManager.getUser());

let currUser = reactive({username: '', name: ''});
(async function() {
    Object.assign(currUser, await sessionManager.getUser());
})();

</script>

<template>
    <main>
        <h1>Home page for AUTHENTICATED users like you: {{ currUser.username }}</h1>
        <router-link :to="{name: 'logout'}" event="">
            <button>Logout</button>
        </router-link> 
        <router-link :to="{name: 'root'}" event="">
            <button>Your profile</button>
        </router-link> 
    </main>
</template>
