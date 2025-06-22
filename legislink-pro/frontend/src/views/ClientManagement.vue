<template>
  <div class="client-management">
    <div class="header mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ $t('client_management.title') }}</h1>
      <p class="text-gray-400">{{ $t('client_management.subtitle', 'Gestión de clientes y casos legales') }}</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Panel de Acciones -->
      <div class="lg:col-span-1">
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-xl font-semibold mb-4">{{ $t('client_management.actions', 'Acciones') }}</h2>
          
          <!-- Crear Cliente -->
          <div class="mb-6">
            <h3 class="text-lg font-medium mb-3">{{ $t('client_management.create_client', 'Crear Cliente') }}</h3>
            <form @submit.prevent="createClient" class="space-y-3">
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('client_management.name', 'Nombre') }}</label>
                <input 
                  v-model="clientForm.name" 
                  type="text"
                  :placeholder="$t('client_management.name_placeholder', 'Nombre completo')"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('client_management.email', 'Email') }}</label>
                <input 
                  v-model="clientForm.email" 
                  type="email"
                  :placeholder="$t('client_management.email_placeholder', 'email@ejemplo.com')"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('client_management.phone', 'Teléfono') }}</label>
                <input 
                  v-model="clientForm.phone" 
                  type="tel"
                  :placeholder="$t('client_management.phone_placeholder', '+56 9 1234 5678')"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
                />
              </div>
              <button 
                type="submit" 
                :disabled="isCreatingClient"
                class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg"
              >
                <span v-if="isCreatingClient">{{ $t('client_management.creating', 'Creando...') }}</span>
                <span v-else>{{ $t('client_management.create', 'Crear Cliente') }}</span>
              </button>
            </form>
          </div>

          <!-- Crear Caso -->
          <div class="mb-6">
            <h3 class="text-lg font-medium mb-3">{{ $t('client_management.create_case', 'Crear Caso') }}</h3>
            <form @submit.prevent="createCase" class="space-y-3">
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('client_management.client_email', 'Email del Cliente') }}</label>
                <input 
                  v-model="caseForm.clientEmail" 
                  type="email"
                  :placeholder="$t('client_management.client_email_placeholder', 'email@ejemplo.com')"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('client_management.case_title', 'Título del Caso') }}</label>
                <input 
                  v-model="caseForm.title" 
                  type="text"
                  :placeholder="$t('client_management.case_title_placeholder', 'Título del caso')"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('client_management.case_description', 'Descripción') }}</label>
                <textarea 
                  v-model="caseForm.description" 
                  rows="3"
                  :placeholder="$t('client_management.case_description_placeholder', 'Descripción del caso...')"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white resize-none"
                ></textarea>
              </div>
              <button 
                type="submit" 
                :disabled="isCreatingCase"
                class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg"
              >
                <span v-if="isCreatingCase">{{ $t('client_management.creating_case', 'Creando...') }}</span>
                <span v-else>{{ $t('client_management.create_case', 'Crear Caso') }}</span>
              </button>
            </form>
          </div>

          <!-- Buscar -->
          <div>
            <h3 class="text-lg font-medium mb-3">{{ $t('client_management.search', 'Buscar') }}</h3>
            <form @submit.prevent="searchClient" class="space-y-3">
              <div>
                <label class="block text-sm font-medium mb-1">{{ $t('client_management.search_email', 'Email del Cliente') }}</label>
                <input 
                  v-model="searchForm.email" 
                  type="email"
                  :placeholder="$t('client_management.search_email_placeholder', 'email@ejemplo.com')"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
                />
              </div>
              <button 
                type="submit" 
                :disabled="isSearching"
                class="w-full bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg"
              >
                <span v-if="isSearching">{{ $t('client_management.searching', 'Buscando...') }}</span>
                <span v-else>{{ $t('client_management.search', 'Buscar Cliente') }}</span>
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Panel de Resultados -->
      <div class="lg:col-span-2">
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-xl font-semibold mb-4">{{ $t('client_management.results', 'Resultados') }}</h2>
          
          <!-- Mensajes del sistema -->
          <div v-if="messages.length > 0" class="mb-4 space-y-2">
            <div v-for="message in messages" :key="message.id" 
                 :class="getMessageClass(message.type)" 
                 class="p-3 rounded-lg">
              {{ message.text }}
            </div>
          </div>

          <!-- Información del cliente -->
          <div v-if="currentClient" class="mb-6">
            <h3 class="text-lg font-semibold mb-3">{{ $t('client_management.client_info', 'Información del Cliente') }}</h3>
            <div class="bg-gray-700 p-4 rounded-lg">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <span class="text-gray-400">{{ $t('client_management.name', 'Nombre:') }}</span>
                  <span class="ml-2 font-medium">{{ currentClient.nombre }}</span>
                </div>
                <div>
                  <span class="text-gray-400">{{ $t('client_management.email', 'Email:') }}</span>
                  <span class="ml-2 font-medium">{{ currentClient.email }}</span>
                </div>
                <div v-if="currentClient.phone">
                  <span class="text-gray-400">{{ $t('client_management.phone', 'Teléfono:') }}</span>
                  <span class="ml-2 font-medium">{{ currentClient.phone }}</span>
                </div>
                <div>
                  <span class="text-gray-400">{{ $t('client_management.id', 'ID:') }}</span>
                  <span class="ml-2 font-medium">{{ currentClient.id }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Casos del cliente -->
          <div v-if="currentClient && clientCases.length > 0" class="mb-6">
            <h3 class="text-lg font-semibold mb-3">{{ $t('client_management.client_cases', 'Casos del Cliente') }}</h3>
            <div class="space-y-3">
              <div v-for="case_item in clientCases" :key="case_item.id" class="bg-gray-700 p-4 rounded-lg">
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium">{{ case_item.titulo }}</h4>
                    <p class="text-sm text-gray-400">{{ case_item.status }}</p>
                    <p v-if="case_item.description" class="text-sm text-gray-300 mt-1">{{ case_item.description }}</p>
                  </div>
                  <span :class="getStatusClass(case_item.status)" class="px-2 py-1 rounded text-xs">
                    {{ case_item.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Lista de todos los clientes -->
          <div v-if="!currentClient">
            <h3 class="text-lg font-semibold mb-3">{{ $t('client_management.all_clients', 'Todos los Clientes') }}</h3>
            <div v-if="allClients.length === 0" class="text-gray-400 text-center py-8">
              {{ $t('client_management.no_clients', 'No hay clientes registrados') }}
            </div>
            <div v-else class="space-y-3">
              <div v-for="client in allClients" :key="client.id" 
                   @click="selectClient(client)"
                   class="bg-gray-700 p-4 rounded-lg cursor-pointer hover:bg-gray-600">
                <div class="flex justify-between items-center">
                  <div>
                    <h4 class="font-medium">{{ client.name }}</h4>
                    <p class="text-sm text-gray-400">{{ client.email }}</p>
                  </div>
                  <div class="text-right">
                    <span class="text-xs text-gray-400">{{ $t('client_management.cases_count', 'Casos:') }} {{ client.cases?.length || 0 }}</span>
                  </div>
                </div>
              </div>
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
  name: 'ClientManagementView',
  data() {
    return {
      clientForm: {
        name: '',
        email: '',
        phone: ''
      },
      caseForm: {
        clientEmail: '',
        title: '',
        description: ''
      },
      searchForm: {
        email: ''
      },
      currentClient: null,
      clientCases: [],
      allClients: [],
      messages: [],
      isCreatingClient: false,
      isCreatingCase: false,
      isSearching: false,
      messageIdCounter: 0
    };
  },
  methods: {
    async createClient() {
      if (!this.clientForm.name.trim() || !this.clientForm.email.trim()) {
        this.addMessage('Nombre y email son requeridos', 'error');
        return;
      }

      this.isCreatingClient = true;
      
      try {
        const response = await api.delegateTask('crear cliente', {
          accion: 'crear_cliente',
          datos: {
            nombre: this.clientForm.name,
            email: this.clientForm.email,
            phone: this.clientForm.phone
          }
        });

        if (response.data.result && response.data.result.mensaje) {
          this.addMessage(response.data.result.mensaje, 'success');
          this.clearClientForm();
          this.loadAllClients();
        } else if (response.data.result && response.data.result.error) {
          this.addMessage(response.data.result.error, 'error');
        }
      } catch (error) {
        console.error('Error:', error);
        this.addMessage('Error al crear el cliente', 'error');
      } finally {
        this.isCreatingClient = false;
      }
    },
    async createCase() {
      if (!this.caseForm.clientEmail.trim() || !this.caseForm.title.trim()) {
        this.addMessage('Email del cliente y título del caso son requeridos', 'error');
        return;
      }

      this.isCreatingCase = true;
      
      try {
        const response = await api.delegateTask('crear caso', {
          accion: 'crear_caso',
          datos: {
            email_cliente: this.caseForm.clientEmail,
            titulo: this.caseForm.title,
            descripcion: this.caseForm.description
          }
        });

        if (response.data.result && response.data.result.mensaje) {
          this.addMessage(response.data.result.mensaje, 'success');
          this.clearCaseForm();
        } else if (response.data.result && response.data.result.error) {
          this.addMessage(response.data.result.error, 'error');
        }
      } catch (error) {
        console.error('Error:', error);
        this.addMessage('Error al crear el caso', 'error');
      } finally {
        this.isCreatingCase = false;
      }
    },
    async searchClient() {
      if (!this.searchForm.email.trim()) {
        this.addMessage('Email es requerido para buscar', 'error');
        return;
      }

      this.isSearching = true;
      
      try {
        const response = await api.delegateTask('buscar cliente', {
          accion: 'buscar_cliente',
          datos: {
            email: this.searchForm.email
          }
        });

        if (response.data.result && response.data.result.id) {
          this.currentClient = response.data.result;
          this.addMessage('Cliente encontrado', 'success');
          this.loadClientCases();
        } else if (response.data.result && response.data.result.error) {
          this.addMessage(response.data.result.error, 'error');
          this.currentClient = null;
        }
      } catch (error) {
        console.error('Error:', error);
        this.addMessage('Error al buscar el cliente', 'error');
      } finally {
        this.isSearching = false;
      }
    },
    async loadAllClients() {
      // Simular carga de clientes - en una implementación real se haría una llamada a la API
      this.allClients = [
        { id: 1, name: 'Juan Pérez', email: 'juan@ejemplo.com', cases: [] },
        { id: 2, name: 'María García', email: 'maria@ejemplo.com', cases: [{ id: 1, title: 'Caso 1' }] }
      ];
    },
    async loadClientCases() {
      if (!this.currentClient) return;
      
      // Simular carga de casos del cliente
      this.clientCases = [
        { id: 1, titulo: 'Revisión de Contrato', status: 'Abierto', description: 'Revisión de contrato comercial' },
        { id: 2, titulo: 'Demanda Laboral', status: 'En Proceso', description: 'Demanda por despido injustificado' }
      ];
    },
    selectClient(client) {
      this.currentClient = {
        id: client.id,
        nombre: client.name,
        email: client.email,
        phone: client.phone
      };
      this.loadClientCases();
    },
    clearClientForm() {
      this.clientForm = { name: '', email: '', phone: '' };
    },
    clearCaseForm() {
      this.caseForm = { clientEmail: '', title: '', description: '' };
    },
    addMessage(text, type) {
      const message = {
        id: this.messageIdCounter++,
        text,
        type
      };
      this.messages.unshift(message);
      
      // Auto-remove messages after 5 seconds
      setTimeout(() => {
        this.messages = this.messages.filter(m => m.id !== message.id);
      }, 5000);
    },
    getMessageClass(type) {
      switch (type) {
        case 'success': return 'bg-green-600 text-white';
        case 'error': return 'bg-red-600 text-white';
        case 'warning': return 'bg-yellow-600 text-white';
        default: return 'bg-blue-600 text-white';
      }
    },
    getStatusClass(status) {
      switch (status?.toLowerCase()) {
        case 'abierto': return 'bg-green-600 text-white';
        case 'en proceso': return 'bg-yellow-600 text-white';
        case 'cerrado': return 'bg-gray-600 text-white';
        default: return 'bg-blue-600 text-white';
      }
    }
  },
  mounted() {
    this.loadAllClients();
  }
};
</script> 