import UHome from './components/UHome.vue';
import LoginPg from './components/LoginPg.vue';
// import UCategory from './components/UCategory.vue';
import USummary from './components/USummary.vue';
import UCart from './components/UCart.vue';
import AUsers from './components/AUsers.vue';
import UProfile from './components/UProfile.vue';  
import PProfile from './components/PProfile.vue';
import PSummary from './components/PSummary.vue';
import PRequests from './components/PRequests.vue';
import SignUp from './components/SignUp.vue';
import AHome from './components/AHome.vue';
import AddServices from './components/AddServices.vue';
import EditServices from './components/EditServices.vue';
import ARequests from './components/ARequests.vue';
import PSignup from './components/PSignup.vue';
import PHome from './components/PHome.vue';
import UnauthorizedAccess from './components/UnauthorizedAccess.vue'
import AProfs from './components/AProfs.vue';
import UOrders from './components/UOrders.vue';
import ASummary from './components/ASummary.vue';

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
    {
        name: 'PProfile',
        component: PProfile,
        meta: { requiresAuth: true, roles: ['Professional'] },
        path: '/pprofile'
    },
    {
        name: 'ARequests',
        component: ARequests,
        meta: { requiresAuth: true, roles: ['Admin'] },
        path: '/arequests'
    },
    {
        name: 'PSummary',
        component: PSummary,
        meta: { requiresAuth: true, roles: ['Professional'] },
        path: '/psummary'
    },
    {
        name: 'PRequests',
        component: PRequests,
        meta: { requiresAuth: true, roles: ['Professional'] },
        path: '/prequests'
    },
    {
        name: 'USummary',
        component:USummary ,
        path: '/usummary'
    },
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
    {
        name: 'AUsers',
        component: AUsers,
        meta: { requiresAuth: true, roles: ['Admin'] },

        path: '/ausers'
    },
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
    },
    {
        name: 'ASummary',
        component: ASummary,
        meta: { requiresAuth: true, roles: ['Admin'] },
        path: '/asummary'
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Add or update the route guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('userrole');

    if (!token || !userRole) {
      next('/login');
      return;
    }

    if (to.meta.roles && !to.meta.roles.includes(userRole)) {
      next('/unauthorized');
      return;
    }

    next();
  } else {
    next();
  }
});

export default router
