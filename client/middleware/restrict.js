import { useAccessStore } from "../store/access"

export default defineNuxtRouteMiddleware((to, from) => {
    const accessStore = useAccessStore();
  
    const restrictedPages = ['/loading', '/results'];

    if (restrictedPages.includes(to.path) && accessStore.pageAccess[to.path]) {
        accessStore.revokeAccess(to.path); 
        return;
    }
    accessStore.revokeAllAccess(); 
    return navigateTo('/'); 
  });