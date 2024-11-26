import UHome from './components/UHome.vue';
import LoginPg from './components/LoginPg.vue';
// import UCategory from './components/UCategory.vue';
// import USummary from './components/USummary.vue';
import UCart from './components/UCart.vue';
// import URecords from './components/URecords.vue';
import UProfile from './components/UProfile.vue';   
import SignUp from './components/SignUp.vue';
import AHome from './components/AHome.vue';
import AddServices from './components/AddServices.vue';
import EditServices from './components/EditServices.vue';
// import ASummary from './components/ASummary.vue';
import PSignup from './components/PSignup.vue';
import PHome from './components/PHome.vue';
import UnauthorizedAccess from './components/UnauthorizedAccess.vue'
import AProfs from './components/AProfs.vue';
import UOrders from './components/UOrders.vue';

import { createRouter, createWebHistory } from 'vue-router'



const routes = [
    {
        name: 'LoginPg',
        component: LoginPg,
        path: '/login'
    },
    {
        name: 'PSignup',
        component: PSignup,
        path: '/psignup'
    },
    {
        name: 'UHome',
        component: UHome,
        path: '/'
    },
    {
        name: 'AProfs',
        component: AProfs,
        path: '/aprofs'
    },
    // {
    //     name: 'UCategory',
    //     component:UCategory ,
    //     path: '/ucategory/:category'
    // },
    // {
    //     name: 'ASummary',
    //     component:ASummary ,
    //     path: '/asummary'
    // },
    {
        name: 'UCart',
        component: UCart ,
        props: true,
        path: '/services/:serviceId'
    },
    {
        name: 'UOrders',
        component: UOrders,
        path: '/uorders'
    },
    // {
    //     name: 'URecords',
    //     component: URecords,
    //     path: '/urecords'
    // },
    {
        name: 'UProfile',
        component: UProfile ,
        path: '/uprofile'
    },
    {
        name: 'SignUp',
        component: SignUp,
        path: '/signup'
    },
    {
        name: 'AHome',
        component: AHome,
        meta: { requiresAuth: true, roles: ['Admin'] },

        path: '/admin'
    },
    {
        name: 'PHome',
        component: PHome,
        meta: { requiresAuth: true, roles: ['Professional'] },

        path: '/professional'
    },
    {
        name: 'AddServices',
        component: AddServices,
        path: '/addservices'
    },
    {
        name: 'EditServices',
        component: EditServices,
        path: '/editservices/:id'
    },
    {
        name: 'UnauthorizedAccess',
        component: UnauthorizedAccess,
        path: '/unauthorized'
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
})

// // Add this before creating the router
// router.beforeEach((to, from, next) => {
//   if (to.meta.requiresAuth) {
//     const token = localStorage.getItem('token');
//     if (!token) {
//       next('/login');
//       return;
//     }
    
//     // You might want to verify the token and role here
//     // For now, we'll just check if token exists
//     next();
//   } else {
//     next();
// 

export default router
