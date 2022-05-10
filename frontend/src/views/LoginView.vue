<script setup>
import {sessionManager} from '@/assets/scripts/user-management.js';
import { useRouter } from 'vue-router';

const router = useRouter();

defineProps({
    returnPath: {
        type: String,
        default: '/',
    }
});

const user = {username: '', password: ''};

async function login(returnPath) {
    // console.log('returnPath: ', returnPath);
    const {username, password} = user;
    try {
        await sessionManager.login(username, password);
        router.push({path: returnPath});
    }
    catch (err) {
        if (err.name === 'LoginError') {   // ou if (err instanceof LoginError)
            alert("Login error: invalid email or password");
            return;
        }
        throw err;
    }
}

</script>

<template>
    <main>
        <form>
            <h1>Login view</h1>
            <input 
                id="username"
                name="username"
                type="text"
                v-model="user.username"
                placeholder="Username or email address..."
            >
            <input 
                id="password"
                name="password"
                type="password" 
                v-model="user.password"
                placeholder="Password..."
            >
            <router-link 
                :to="returnPath"
                event=""
                @click="login(returnPath)"
            >
                <button>Sign in to WebQuiz</button>
            </router-link> 
        </form> 
        <div id="sign-up">
            New to WebQuiz?
            <router-link :to="{name: 'signup'}" event="">
                Sign up
            </router-link>
        </div>
    </main>
</template>

<style scoped>
form {
    width: 30em;
    height: 20em;
    border: 1px solid;
    padding: 2em;

    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: space-between;
}
#sign-up {
    margin-top: 1em;
}
button {
    width: 100%;    
}
</style>