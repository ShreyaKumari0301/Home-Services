
import { createApp } from 'vue'
import App from './App.vue'
import router from './routers'
import { getUserRole } from './Auth';


router.beforeEach((to, from, next) => {
    const requiresAuth = to.meta.requiresAuth;
    const requiredRoles = to.meta.roles;
  
    if (requiresAuth) {
      if (!getUserRole()) {
        return next('/login');
      } else if (requiredRoles && !requiredRoles.includes(getUserRole())) {
        return next('/unauthorized');
      }
    }
  
    next(); // Allow access
  });
  


const app = createApp(App)


app.use(router);
app.mount('#app');
