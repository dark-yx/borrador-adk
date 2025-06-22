<template>
  <div class="legal-search">
    <div class="header mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ $t('legal_search.title') }}</h1>
      <p class="text-gray-400">{{ $t('legal_search.subtitle', 'Búsqueda semántica en base de conocimiento legal') }}</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de Búsqueda -->
      <div class="lg:col-span-1">
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-xl font-semibold mb-4">{{ $t('legal_search.search_panel', 'Búsqueda') }}</h2>
          
          <form @submit.prevent="performSearch" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">{{ $t('legal_search.query', 'Consulta Legal') }}</label>
              <textarea 
                v-model="searchForm.query" 
                rows="4"
                :placeholder="$t('legal_search.query_placeholder', 'Escribe tu consulta legal...')"
                class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white resize-none"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">{{ $t('legal_search.search_type', 'Tipo de Búsqueda') }}</label>
              <select v-model="searchForm.type" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white">
                <option value="semantic">{{ $t('legal_search.semantic', 'Semántica (RAG)') }}</option>
                <option value="constitutional">{{ $t('legal_search.constitutional', 'Constitucional') }}</option>
                <option value="document">{{ $t('legal_search.document', 'Documentos') }}</option>
              </select>
            </div>

            <div v-if="searchForm.type === 'constitutional'">
              <label class="block text-sm font-medium mb-2">{{ $t('legal_search.country', 'País') }}</label>
              <select v-model="searchForm.country" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white">
                <option value="cl">Chile</option>
                <option value="mx">México</option>
                <option value="co">Colombia</option>
                <option value="ar">Argentina</option>
                <option value="pe">Perú</option>
                <option value="es">España</option>
              </select>
            </div>

            <button 
              type="submit" 
              :disabled="isSearching"
              class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 px-4 rounded-lg"
            >
              <span v-if="isSearching">{{ $t('legal_search.searching', 'Buscando...') }}</span>
              <span v-else>{{ $t('legal_search.search', 'Buscar') }}</span>
            </button>
          </form>

          <!-- Historial de Búsquedas -->
          <div class="mt-6">
            <h3 class="text-lg font-medium mb-3">{{ $t('legal_search.recent_searches', 'Búsquedas Recientes') }}</h3>
            <div class="space-y-2">
              <div 
                v-for="search in recentSearches" 
                :key="search.id"
                @click="loadSearch(search)"
                class="p-2 bg-gray-700 rounded cursor-pointer hover:bg-gray-600"
              >
                <div class="text-sm font-medium">{{ search.query }}</div>
                <div class="text-xs text-gray-400">{{ search.timestamp }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel de Resultados -->
      <div class="lg:col-span-2">
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-xl font-semibold mb-4">{{ $t('legal_search.results', 'Resultados') }}</h2>
          
          <div v-if="!currentSearch" class="text-gray-400 text-center py-12">
            {{ $t('legal_search.no_search', 'Realiza una búsqueda para ver los resultados') }}
          </div>
          
          <div v-else class="space-y-4">
            <!-- Información de la búsqueda -->
            <div class="bg-gray-700 p-4 rounded-lg">
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="font-semibold">{{ currentSearch.query }}</h3>
                  <p class="text-sm text-gray-400">{{ currentSearch.timestamp }}</p>
                </div>
                <span :class="getStatusClass(currentSearch.status)" class="px-2 py-1 rounded text-xs">
                  {{ currentSearch.status }}
                </span>
              </div>
            </div>

            <!-- Resultados de RAG -->
            <div v-if="currentSearch.type === 'semantic' && currentSearch.results" class="space-y-4">
              <div class="bg-gray-700 p-4 rounded-lg">
                <h4 class="font-semibold mb-2">{{ $t('legal_search.answer', 'Respuesta') }}</h4>
                <p class="text-gray-300">{{ currentSearch.results.respuesta }}</p>
              </div>
              
              <div class="bg-gray-700 p-4 rounded-lg">
                <h4 class="font-semibold mb-2">{{ $t('legal_search.context', 'Contexto Utilizado') }}</h4>
                <p class="text-sm text-gray-400">{{ currentSearch.results.contexto_usado }}</p>
              </div>
              
              <div class="bg-gray-700 p-4 rounded-lg">
                <h4 class="font-semibold mb-2">{{ $t('legal_search.metrics', 'Métricas') }}</h4>
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span class="text-gray-400">{{ $t('legal_search.results_count', 'Resultados:') }}</span>
                    <span class="ml-2">{{ currentSearch.results.num_resultados }}</span>
                  </div>
                  <div>
                    <span class="text-gray-400">{{ $t('legal_search.confidence', 'Confianza:') }}</span>
                    <span class="ml-2">{{ calculateConfidence(currentSearch.results.num_resultados) }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Resultados Constitucionales -->
            <div v-if="currentSearch.type === 'constitutional' && currentSearch.results" class="space-y-4">
              <div class="bg-gray-700 p-4 rounded-lg">
                <h4 class="font-semibold mb-2">{{ $t('legal_search.constitutional_analysis', 'Análisis Constitucional') }}</h4>
                <div class="grid grid-cols-2 gap-4 text-sm mb-3">
                  <div>
                    <span class="text-gray-400">{{ $t('legal_search.compatibility', 'Compatibilidad:') }}</span>
                    <span :class="currentSearch.results.es_compatible ? 'text-green-400' : 'text-red-400'" class="ml-2">
                      {{ currentSearch.results.es_compatible ? 'Compatible' : 'No Compatible' }}
                    </span>
                  </div>
                  <div>
                    <span class="text-gray-400">{{ $t('legal_search.confidence_score', 'Score:') }}</span>
                    <span class="ml-2">{{ currentSearch.results.confidence_score }}</span>
                  </div>
                </div>
              </div>
              
              <div v-if="currentSearch.results.articulos_relevantes && currentSearch.results.articulos_relevantes.length > 0" class="space-y-3">
                <h4 class="font-semibold">{{ $t('legal_search.relevant_articles', 'Artículos Relevantes') }}</h4>
                <div v-for="(articulo, index) in currentSearch.results.articulos_relevantes" :key="index" class="bg-gray-700 p-3 rounded-lg">
                  <div class="font-medium text-blue-400">{{ articulo.articulo }}</div>
                  <div class="text-sm text-gray-300 mt-1">{{ articulo.texto }}</div>
                  <a v-if="articulo.url" :href="articulo.url" target="_blank" class="text-xs text-green-400 hover:underline">
                    {{ $t('legal_search.view_article', 'Ver artículo') }}
                  </a>
                </div>
              </div>
            </div>

            <!-- Acciones -->
            <div class="flex gap-2">
              <button 
                @click="saveSearch" 
                class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg"
              >
                {{ $t('legal_search.save', 'Guardar Búsqueda') }}
              </button>
              <button 
                @click="exportResults" 
                class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg"
              >
                {{ $t('legal_search.export', 'Exportar') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'LegalSearchView',
  data() {
    return {
      searchForm: {
        query: '',
        type: 'semantic',
        country: 'cl'
      },
      currentSearch: null,
      recentSearches: [],
      isSearching: false,
      searchIdCounter: 0
    };
  },
  methods: {
    async performSearch() {
      if (!this.searchForm.query.trim()) {
        return;
      }

      this.isSearching = true;
      
      try {
        let response;
        const query = this.searchForm.query;
        
        if (this.searchForm.type === 'semantic') {
          response = await api.delegateTask('buscar en conocimiento legal', {
            pregunta: query
          });
        } else if (this.searchForm.type === 'constitutional') {
          response = await api.delegateTask('validar proceso constitucional', {
            proceso: query,
            pais: this.searchForm.country
          });
        } else {
          response = await api.delegateTask('buscar documentos', {
            query: query
          });
        }

        if (response.data.result) {
          this.currentSearch = {
            id: this.searchIdCounter++,
            query: query,
            type: this.searchForm.type,
            results: response.data.result,
            status: 'completed',
            timestamp: new Date().toLocaleString()
          };
          
          this.addToRecentSearches(this.currentSearch);
        } else {
          this.currentSearch = {
            id: this.searchIdCounter++,
            query: query,
            type: this.searchForm.type,
            results: null,
            status: 'error',
            timestamp: new Date().toLocaleString()
          };
        }
      } catch (error) {
        console.error('Error:', error);
        this.currentSearch = {
          id: this.searchIdCounter++,
          query: this.searchForm.query,
          type: this.searchForm.type,
          results: null,
          status: 'error',
          timestamp: new Date().toLocaleString()
        };
      } finally {
        this.isSearching = false;
      }
    },
    addToRecentSearches(search) {
      this.recentSearches.unshift(search);
      if (this.recentSearches.length > 10) {
        this.recentSearches = this.recentSearches.slice(0, 10);
      }
    },
    loadSearch(search) {
      this.searchForm.query = search.query;
      this.searchForm.type = search.type;
      this.currentSearch = search;
    },
    getStatusClass(status) {
      switch (status) {
        case 'completed': return 'bg-green-600 text-white';
        case 'error': return 'bg-red-600 text-white';
        case 'searching': return 'bg-yellow-600 text-white';
        default: return 'bg-gray-600 text-white';
      }
    },
    calculateConfidence(numResults) {
      return Math.min(100, Math.max(0, numResults * 20));
    },
    saveSearch() {
      // Implementar guardado en localStorage o backend
      localStorage.setItem(`search_${this.currentSearch.id}`, JSON.stringify(this.currentSearch));
    },
    exportResults() {
      if (!this.currentSearch || !this.currentSearch.results) return;
      
      const data = {
        search: this.currentSearch,
        exportDate: new Date().toISOString()
      };
      
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `legal_search_${this.currentSearch.id}_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }
  }
};
</script> 