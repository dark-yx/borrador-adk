<template>
  <div class="bg-gray-900 text-white min-h-screen flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 p-4 flex flex-col">
      <h1 class="text-2xl font-bold mb-8">LegisLink</h1>
      <nav class="flex flex-col space-y-2">
        <router-link to="/" class="px-4 py-2 rounded" active-class="bg-gray-700">{{ $t('nav.dashboard') }}</router-link>
        <router-link to="/documents" class="px-4 py-2 rounded hover:bg-gray-700" active-class="bg-gray-700">{{ $t('nav.generate_document') }}</router-link>
        <router-link to="/search" class="px-4 py-2 rounded hover:bg-gray-700" active-class="bg-gray-700">{{ $t('nav.legal_search') }}</router-link>
        <router-link to="/clients" class="px-4 py-2 rounded hover:bg-gray-700" active-class="bg-gray-700">{{ $t('nav.clients') }}</router-link>
      </nav>
      <div class="mt-auto">
        <LanguageSwitcher />
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <router-view />
    </main>
  </div>
</template>

<script>
import LanguageSwitcher from './components/LanguageSwitcher.vue';

export default {
  name: 'App',
  components: {
    LanguageSwitcher
  }
}
</script>

<style>
/* Se pueden quitar los estilos antiguos de #app, ya que Tailwind maneja el layout */
body {
  margin: 0;
  background-color: #111827; /* bg-gray-900 */
}

.router-link-exact-active {
  background-color: #374151; /* bg-gray-700 */
}
</style>
