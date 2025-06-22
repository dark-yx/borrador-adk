import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  { 
    path: '/search', 
    name: 'LegalSearch', 
    component: () => import('../views/LegalSearch.vue') 
  },
  { 
    path: '/documents', 
    name: 'DocumentGeneration', 
    component: () => import('../views/DocumentGeneration.vue') 
  },
  { 
    path: '/clients', 
    name: 'ClientManagement', 
    component: () => import('../views/ClientManagement.vue') 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router; 