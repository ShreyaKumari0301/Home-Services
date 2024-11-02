import HelloShreya from './components/HelloShreya.vue';
import { createRouter, createWebHistory } from 'vue-router'



const routes = [
    {
        name: 'Home',
        component: HelloShreya,
        path: '/'
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
