import { createI18n } from 'vue-i18n';
import en from './locales/en.json';
import es from './locales/es.json';

const i18n = createI18n({
  locale: 'es', // idioma por defecto
  fallbackLocale: 'en', // idioma de respaldo
  messages: {
    en,
    es
  },
  legacy: false, // para usar la API de Composition de Vue 3
});

export default i18n; 