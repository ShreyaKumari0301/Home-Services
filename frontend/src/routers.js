import UHome from './components/UHome.vue';
import LoginPg from './components/LoginPg.vue';
// import UCategory from './components/UCategory.vue';
// import USummary from './components/USummary.vue';
import UCart from './components/UCart.vue';
// import URecords from './components/URecords.vue';
// import UProfile from './components/UProfile.vue';   
import SignUp from './components/SignUp.vue';
import AHome from './components/AHome.vue';
import AddServices from './components/AddServices.vue';
import EditServices from './components/EditServices.vue';
// import ASummary from './components/ASummary.vue';

import { createRouter, createWebHistory } from 'vue-router'



const routes = [
    {
        name: 'LoginPg',
        component: LoginPg,
        path: '/login'
    },
    {
        name: 'UHome',
        component: UHome,
        path: '/'
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
        path: '/ucart'
    },
    // {
    //     name: 'URecords',
    //     component: URecords,
    //     path: '/urecords'
    // },
    // {
    //     name: 'UProfile',
    //     component: UProfile ,
    //     path: '/uprofile'
    // },
    // {
    //     name: 'PSignup',
    //     component: SignUp,
    //     path: '/psignup'
    // },
    {
        name: 'SignUp',
        component: SignUp,
        path: '/signup'
    },
    {
        name: 'AHome',
        component: AHome,
        path: '/admin'
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
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
