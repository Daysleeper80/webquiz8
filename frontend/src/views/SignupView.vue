<script setup>
import {sessionManager} from '@/assets/scripts/user-management.js';
import { useRouter } from 'vue-router';

const router = useRouter();

const newUser = {
    username: {
        regex: /^[a-zA-Z0-9]{3,10}$/,
        errorMsgID: 'err-username',
        value: '',
    },
    firstName: {
        regex: /^[a-zA-Z]{2,20}$/,
        errorMsgID: 'err-first-name',
        value: '',
    },
    emailAddr: {
        regex: /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/,
        errorMsgID: 'err-email-addr',
        value: '',
    },
    password: {
        // regexp: /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!$#?%]).{6,}$/,
        regex: /^(?=.*[a-z]).{3,}$/,
        errorMsgID: 'err-password',
        value: '',
    },
};

function validateElem(elem) {
    const {regex, errorMsgID} = elem;
    if (regex.test(elem.value)) {
        hideInlineElem(errorMsgID);
        return true;
    }
    showInlineElem(errorMsgID);
    return false;
}

function showInlineElem(id) {
    let elem = document.getElementById(id);
    elem.style.display = 'inline';
}

function hideInlineElem(id) {
    let elem = document.getElementById(id);
    elem.style.display = 'none';
}

async function createUser() {
    const allValid = Object.values(newUser).every(elem => elem.regex.test(elem.value));
    if (!allValid) {
        alert("Problems with form values...");
        return;
    }

    const newUserDetails = {};
    for (let key of Object.keys(newUser)) {
        newUserDetails[key] = newUser[key].value;
    }

    try {
        let createdUser = await sessionManager.createUser(newUserDetails);
        alert(`User registered (${createdUser.emailAddr})`);
        router.push({name: 'home'});
    }
    catch (err) {
        if (err.name === 'UserError') {   // ou if (err instanceof UserError)
            alert("Error creating user: invalid or existing user details...");
            return;
        }
        throw err;
    }
}

</script>

<template>
    <main>
        <form @submit.prevent="createUser()">
            <h1>Sign up </h1>
            <input 
                id="username"
                name="username"
                type="text"
                v-model="newUser.username.value"
                placeholder="Enter your username..."
                @focusout="validateElem(newUser.username)"
            >
            <span id="err-username" class="error-msg">Invalid user name...</span>
            <input 
                id="firstName"
                name="firstName"
                type="text"
                v-model="newUser.firstName.value"
                placeholder="What's your personal name..."
                @focusout="validateElem(newUser.firstName)"
            >
            <span id="err-first-name" class="error-msg">Invalid first name...</span>
            <input 
                id="password"
                name="password"
                type="password" 
                v-model="newUser.password.value"
                placeholder="Password..."
                @focusout="validateElem(newUser.password)"
            >
            <span id="err-password" class="error-msg">Invalid password...</span>
            <input 
                id="emailAddr"
                name="emailAddr"
                type="text"
                v-model="newUser.emailAddr.value"
                placeholder="Enter your em@ail address..."
                @focusout="validateElem(newUser.emailAddr)"
            >
            <span id="err-email-addr" class="error-msg">Invalid email address...</span>

            <button>Continue...</button>

            <!-- 
            <router-link 
                :to="{name: 'home'}" 
                event=""
                @click="registerUser()"
            >
                <button>Continue...</button>
            </router-link>  
            -->

        </form> 
        <div id="login">
            Already have an account?
            <router-link :to="{name: 'login'}" event="">
                Sign in
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
.error-msg {
    display: none;
}
</style>