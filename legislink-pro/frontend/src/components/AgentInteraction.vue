<template>
  <div class="agent-interaction">
    <div class="bg-gray-800 p-6 rounded-lg">
      <h2 class="text-xl font-semibold mb-4">{{ title }}</h2>
      
      <!-- Chat Messages -->
      <div class="h-96 overflow-y-auto bg-gray-900 rounded-lg p-4 mb-4">
        <div v-if="messages.length === 0" class="text-gray-400 text-center py-8">
          {{ placeholder }}
        </div>
        
        <div v-for="message in messages" :key="message.id" class="mb-4">
          <div :class="message.sender === 'user' ? 'text-right' : 'text-left'">
            <div :class="message.sender === 'user' ? 'bg-blue-600' : 'bg-gray-700'" 
                 class="inline-block p-3 rounded-lg max-w-xs lg:max-w-md">
              <div v-if="message.sender === 'agent' && message.data" class="space-y-2">
                <div v-if="message.data.document" class="space-y-2">
                  <div class="font-semibold">{{ $t('agent_interaction.document_generated', 'Documento Generado') }}</div>
                  <div class="text-sm bg-gray-800 p-2 rounded border-l-4 border-green-500">
                    <pre class="whitespace-pre-wrap text-xs">{{ message.data.document }}</pre>
                  </div>
                </div>
                <div v-if="message.data.results" class="space-y-2">
                  <div class="font-semibold">{{ $t('agent_interaction.results', 'Resultados') }}</div>
                  <div class="text-sm bg-gray-800 p-2 rounded border-l-4 border-blue-500">
                    <pre class="whitespace-pre-wrap text-xs">{{ JSON.stringify(message.data.results, null, 2) }}</pre>
                  </div>
                </div>
                <div v-if="message.data.error" class="text-red-400 text-sm">
                  {{ message.data.error }}
                </div>
              </div>
              <div v-else>
                {{ message.text }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Form -->
      <form @submit.prevent="sendMessage" class="space-y-4">
        <div v-if="showTaskSelector">
          <label class="block text-sm font-medium mb-2">{{ $t('agent_interaction.task_type', 'Tipo de Tarea') }}</label>
          <select v-model="selectedTask" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white">
            <option value="">{{ $t('agent_interaction.select_task', 'Seleccionar tarea...') }}</option>
            <option value="generar documento">{{ $t('agent_interaction.generate_document', 'Generar Documento') }}</option>
            <option value="buscar en conocimiento legal">{{ $t('agent_interaction.legal_search', 'Búsqueda Legal') }}</option>
            <option value="validar proceso constitucional">{{ $t('agent_interaction.constitutional_validation', 'Validación Constitucional') }}</option>
            <option value="crear cliente">{{ $t('agent_interaction.create_client', 'Crear Cliente') }}</option>
            <option value="crear caso">{{ $t('agent_interaction.create_case', 'Crear Caso') }}</option>
            <option value="buscar cliente">{{ $t('agent_interaction.search_client', 'Buscar Cliente') }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium mb-2">{{ $t('agent_interaction.message', 'Mensaje') }}</label>
          <textarea 
            v-model="inputMessage" 
            rows="3"
            :placeholder="placeholder"
            class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white resize-none"
            :disabled="isProcessing"
          ></textarea>
        </div>

        <div v-if="showAdditionalFields" class="space-y-3">
          <div v-if="selectedTask === 'generar documento'">
            <label class="block text-sm font-medium mb-2">{{ $t('agent_interaction.document_type', 'Tipo de Documento') }}</label>
            <select v-model="additionalData.tipo" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white">
              <option value="contrato">Contrato</option>
              <option value="acuerdo">Acuerdo</option>
              <option value="poder">Poder</option>
              <option value="testamento">Testamento</option>
              <option value="demanda">Demanda</option>
            </select>
          </div>

          <div v-if="selectedTask === 'validar proceso constitucional'">
            <label class="block text-sm font-medium mb-2">{{ $t('agent_interaction.country', 'País') }}</label>
            <select v-model="additionalData.pais" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white">
              <option value="cl">Chile</option>
              <option value="mx">México</option>
              <option value="co">Colombia</option>
              <option value="ar">Argentina</option>
              <option value="pe">Perú</option>
              <option value="es">España</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="isProcessing || !canSubmit"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 px-4 rounded-lg"
        >
          <span v-if="isProcessing">{{ $t('agent_interaction.processing', 'Procesando...') }}</span>
          <span v-else>{{ $t('agent_interaction.send', 'Enviar') }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'AgentInteraction',
  props: {
    title: {
      type: String,
      default: 'Interacción con Agentes'
    },
    placeholder: {
      type: String,
      default: 'Escribe tu mensaje aquí...'
    },
    showTaskSelector: {
      type: Boolean,
      default: true
    },
    initialTask: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      messages: [],
      inputMessage: '',
      selectedTask: this.initialTask,
      additionalData: {},
      isProcessing: false,
      messageIdCounter: 0
    };
  },
  computed: {
    showAdditionalFields() {
      return this.selectedTask && ['generar documento', 'validar proceso constitucional'].includes(this.selectedTask);
    },
    canSubmit() {
      if (this.showTaskSelector && !this.selectedTask) return false;
      if (!this.inputMessage.trim()) return false;
      return true;
    }
  },
  methods: {
    async sendMessage() {
      if (!this.canSubmit) return;

      this.isProcessing = true;
      
      // Add user message
      this.addMessage(this.inputMessage, 'user');
      
      const userMessage = this.inputMessage;
      this.inputMessage = '';

      try {
        let taskData = {};
        
        if (this.selectedTask) {
          taskData = {
            ...this.additionalData,
            ...this.parseUserInput(userMessage)
          };
        } else {
          taskData = { mensaje: userMessage };
        }

        const response = await api.delegateTask(this.selectedTask || 'procesar mensaje', taskData);

        if (response.data.result) {
          this.addMessage({
            text: this.formatResponse(response.data.result),
            data: response.data.result
          }, 'agent');
        } else {
          this.addMessage('Error al procesar la solicitud', 'agent');
        }
      } catch (error) {
        console.error('Error:', error);
        this.addMessage('Error al procesar la solicitud. Inténtalo de nuevo.', 'agent');
      } finally {
        this.isProcessing = false;
      }
    },
    addMessage(content, sender) {
      const message = {
        id: this.messageIdCounter++,
        sender,
        text: typeof content === 'string' ? content : content.text,
        data: content.data
      };
      this.messages.push(message);
      
      // Auto-scroll to bottom
      this.$nextTick(() => {
        const container = this.$el.querySelector('.overflow-y-auto');
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    parseUserInput(input) {
      // Simple parsing based on task type
      if (this.selectedTask === 'generar documento') {
        return {
          descripcion: input
        };
      } else if (this.selectedTask === 'buscar en conocimiento legal') {
        return {
          pregunta: input
        };
      } else if (this.selectedTask === 'validar proceso constitucional') {
        return {
          proceso: input
        };
      } else if (this.selectedTask === 'crear cliente') {
        // Try to parse name and email from input
        const emailMatch = input.match(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/);
        const email = emailMatch ? emailMatch[0] : '';
        const name = input.replace(email, '').trim();
        
        return {
          nombre: name,
          email: email
        };
      }
      
      return { mensaje: input };
    },
    formatResponse(result) {
      if (result.mensaje) return result.mensaje;
      if (result.respuesta) return result.respuesta;
      if (result.documento_generado) return 'Documento generado exitosamente';
      if (result.error) return `Error: ${result.error}`;
      return 'Respuesta recibida del agente';
    },
    clearMessages() {
      this.messages = [];
      this.messageIdCounter = 0;
    }
  }
};
</script> 