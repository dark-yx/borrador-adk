import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import i18n from './i18n'
import router from './router'
import './assets/css/tailwind.css'

// Cargar el idioma guardado antes de crear la app
const savedLocale = localStorage.getItem('user-locale');
if (savedLocale) {
  i18n.global.locale.value = savedLocale;
}

const pinia = createPinia()

createApp(App)
  .use(pinia)
  .use(i18n)
  .use(router)
  .mount('#app')
