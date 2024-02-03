<template>
  <div id="app">
    <router-view></router-view>
  </div>
  <button v-if="isAppPage" @click="goToRegister">Register</button>
  <button v-if="isAppPage" @click="goToFilm">films</button>
  <div>
    <h1 v-if="isAppPage">welcome</h1>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';

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

const isAppPage = computed(() => route.path === '/');

</script>