import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../pages/Login.vue';
import RegisterPage from '../pages/Register.vue';
import UserPage from "../pages/Userself.vue";
import FilmsPage from "../pages/Films.vue"


const routes = [
    {
        path: '/register',
        name: 'Register',
        component: RegisterPage,
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage,
    },
    {
        path: '/user/:username',
        name: 'User',
        component: UserPage,
    },
    {
        path: '/films',
        name: 'Films',
        component: FilmsPage,
    },
    //
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;