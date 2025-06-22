<template>
  <div class="dashboard">
    <div class="header mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ $t('dashboard.title') }}</h1>
      <p class="text-gray-400">{{ $t('dashboard.subtitle', 'Panel de control de LegisLink Pro') }}</p>
    </div>

    <!-- Métricas principales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-gray-800 p-6 rounded-lg">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-600">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-400">{{ $t('dashboard.total_clients', 'Total Clientes') }}</p>
            <p class="text-2xl font-semibold text-white">{{ metrics.totalClients }}</p>
          </div>
        </div>
      </div>

      <div class="bg-gray-800 p-6 rounded-lg">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-600">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-400">{{ $t('dashboard.total_cases', 'Total Casos') }}</p>
            <p class="text-2xl font-semibold text-white">{{ metrics.totalCases }}</p>
          </div>
        </div>
      </div>

      <div class="bg-gray-800 p-6 rounded-lg">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-600">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-400">{{ $t('dashboard.active_cases', 'Casos Activos') }}</p>
            <p class="text-2xl font-semibold text-white">{{ metrics.activeCases }}</p>
          </div>
        </div>
      </div>

      <div class="bg-gray-800 p-6 rounded-lg">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-600">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-400">{{ $t('dashboard.documents_generated', 'Documentos Generados') }}</p>
            <p class="text-2xl font-semibold text-white">{{ metrics.documentsGenerated }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Actividad Reciente -->
      <div class="bg-gray-800 p-6 rounded-lg">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.recent_activity', 'Actividad Reciente') }}</h2>
        <div class="space-y-4">
          <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3">
            <div :class="getActivityIconClass(activity.type)" class="p-2 rounded-full">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="activity.type === 'client'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                <path v-else-if="activity.type === 'case'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-white">{{ activity.title }}</p>
              <p class="text-xs text-gray-400">{{ activity.description }}</p>
              <p class="text-xs text-gray-500 mt-1">{{ activity.timestamp }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado de Agentes -->
      <div class="bg-gray-800 p-6 rounded-lg">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.agent_status', 'Estado de Agentes') }}</h2>
        <div class="space-y-3">
          <div v-for="agent in agentStatus" :key="agent.name" class="flex items-center justify-between">
            <div class="flex items-center">
              <div :class="getStatusIndicatorClass(agent.status)" class="w-3 h-3 rounded-full mr-3"></div>
              <span class="text-sm font-medium text-white">{{ agent.name }}</span>
            </div>
            <span :class="getStatusTextClass(agent.status)" class="text-xs px-2 py-1 rounded">
              {{ agent.status }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Acciones Rápidas -->
    <div class="mt-8">
      <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.quick_actions', 'Acciones Rápidas') }}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <button 
          @click="$router.push('/document-generation')"
          class="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-lg text-center transition-colors"
        >
          <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <span class="font-medium">{{ $t('dashboard.generate_document', 'Generar Documento') }}</span>
        </button>

        <button 
          @click="$router.push('/legal-search')"
          class="bg-green-600 hover:bg-green-700 text-white p-4 rounded-lg text-center transition-colors"
        >
          <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <span class="font-medium">{{ $t('dashboard.search_legal', 'Búsqueda Legal') }}</span>
        </button>

        <button 
          @click="$router.push('/client-management')"
          class="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-lg text-center transition-colors"
        >
          <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
          </svg>
          <span class="font-medium">{{ $t('dashboard.manage_clients', 'Gestionar Clientes') }}</span>
        </button>

        <button 
          @click="refreshMetrics"
          class="bg-yellow-600 hover:bg-yellow-700 text-white p-4 rounded-lg text-center transition-colors"
        >
          <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span class="font-medium">{{ $t('dashboard.refresh', 'Actualizar') }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'DashboardView',
  data() {
    return {
      metrics: {
        totalClients: 0,
        totalCases: 0,
        activeCases: 0,
        documentsGenerated: 0
      },
      recentActivity: [],
      agentStatus: [
        { name: 'CRM Agent', status: 'online' },
        { name: 'RAG Agent', status: 'online' },
        { name: 'Constitute Agent', status: 'online' },
        { name: 'Document Agent', status: 'online' },
        { name: 'Translation Agent', status: 'offline' }
      ]
    };
  },
  methods: {
    async loadMetrics() {
      try {
        // Simular carga de métricas desde la API
        this.metrics = {
          totalClients: 25,
          totalCases: 42,
          activeCases: 18,
          documentsGenerated: 156
        };
      } catch (error) {
        console.error('Error loading metrics:', error);
      }
    },
    async loadRecentActivity() {
      try {
        // Simular carga de actividad reciente
        this.recentActivity = [
          {
            id: 1,
            type: 'client',
            title: 'Nuevo cliente registrado',
            description: 'Juan Pérez se registró en el sistema',
            timestamp: 'Hace 2 horas'
          },
          {
            id: 2,
            type: 'case',
            title: 'Caso actualizado',
            description: 'Caso #1234 marcado como "En Proceso"',
            timestamp: 'Hace 4 horas'
          },
          {
            id: 3,
            type: 'document',
            title: 'Documento generado',
            description: 'Contrato comercial generado para María García',
            timestamp: 'Hace 6 horas'
          },
          {
            id: 4,
            type: 'search',
            title: 'Búsqueda legal realizada',
            description: 'Consulta sobre derecho laboral',
            timestamp: 'Hace 8 horas'
          }
        ];
      } catch (error) {
        console.error('Error loading recent activity:', error);
      }
    },
    async refreshMetrics() {
      await this.loadMetrics();
      await this.loadRecentActivity();
    },
    getActivityIconClass(type) {
      switch (type) {
        case 'client': return 'bg-blue-600';
        case 'case': return 'bg-green-600';
        case 'document': return 'bg-purple-600';
        case 'search': return 'bg-yellow-600';
        default: return 'bg-gray-600';
      }
    },
    getStatusIndicatorClass(status) {
      switch (status) {
        case 'online': return 'bg-green-500';
        case 'offline': return 'bg-red-500';
        case 'busy': return 'bg-yellow-500';
        default: return 'bg-gray-500';
      }
    },
    getStatusTextClass(status) {
      switch (status) {
        case 'online': return 'bg-green-600 text-white';
        case 'offline': return 'bg-red-600 text-white';
        case 'busy': return 'bg-yellow-600 text-white';
        default: return 'bg-gray-600 text-white';
      }
    }
  },
  mounted() {
    this.loadMetrics();
    this.loadRecentActivity();
  }
};
</script> 