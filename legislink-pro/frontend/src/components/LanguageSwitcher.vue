<template>
  <div class="language-switcher">
    <button @click="setLocale('es')" :class="{ active: $i18n.locale === 'es' }">Español</button>
    <button @click="setLocale('en')" :class="{ active: $i18n.locale === 'en' }">English</button>
  </div>
</template>

<script>
export default {
  name: 'LanguageSwitcher',
  methods: {
    setLocale(locale) {
      this.$i18n.locale = locale;
      localStorage.setItem('user-locale', locale);
    }
  }
}
</script>

<style scoped>
.language-switcher {
  margin: 1em;
}
button {
  padding: 0.5em 1em;
  margin: 0 0.5em;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  cursor: pointer;
}
button.active {
  background-color: #42b983;
  color: white;
  font-weight: bold;
}
</style> 