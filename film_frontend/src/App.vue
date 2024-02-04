<template>
  <div id="app" class="app-container">
    <router-view></router-view>

    <h1 v-if="isAppPage" class="welcome-title">Welcome to the Film Comments System</h1>
    <div v-if="isAppPage" class="navigation-buttons">
      <button @click="goToRegister">Register</button>
      <button @click="goToLogin">Login</button>
      <button @click="goToFilm">Films</button>
    </div>
  </div>
</template>

<script setup>
import {useRouter, useRoute} from 'vue-router';
import {computed} from 'vue';

const router = useRouter();
const route = useRoute();

function goToRegister() {
  console.log('goToRegister function called');
  router.replace('/register');
}

function goToFilm() {
  console.log('goToFilm function called');
  router.replace('/films');
}

function goToLogin() {
  console.log('goToLogin function called');
  router.replace('/login');
}

const isAppPage = computed(() => route.path === '/');
</script>

<style>
.app-container {
  text-align: center;
  padding: 20px;
}

.navigation-buttons {
  margin-bottom: 20px;
}

.navigation-buttons button {
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.welcome-title {
  margin-top: 20px;
  font-size: 2em;
  color: #333;
}
</style>