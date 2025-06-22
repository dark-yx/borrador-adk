<template>
  <div class="agent-interaction-container bg-gray-800 p-4 rounded-lg h-full flex flex-col">
    <!-- Message Display Area -->
    <div class="message-display-area flex-1 overflow-y-auto mb-4 p-2 bg-gray-900 rounded">
      <div v-for="message in messages" :key="message.id" class="message mb-2" :class="message.sender === 'user' ? 'text-right' : 'text-left'">
        <span class="inline-block p-2 rounded-lg" :class="message.sender === 'user' ? 'bg-blue-600' : 'bg-gray-700'">
          {{ message.text }}
        </span>
      </div>
    </div>

    <!-- Input Form -->
    <form @submit.prevent="sendMessage" class="flex items-center">
      <input
        type="text"
        v-model="newMessage"
        :placeholder="placeholder"
        class="flex-1 bg-gray-700 text-white rounded-l-lg p-2 focus:outline-none"
        :disabled="isLoading"
      />
      <button
        type="submit"
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-r-lg"
        :disabled="isLoading"
      >
        <span v-if="isLoading">...</span>
        <span v-else>Enviar</span>
      </button>
    </form>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'AgentInteraction',
  props: {
    initialPrompt: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Escribe tu mensaje aquí...'
    }
  },
  data() {
    return {
      messages: [],
      newMessage: '',
      isLoading: false,
      messageIdCounter: 0,
    };
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() === '' || this.isLoading) return;

      const userMessage = {
        id: this.messageIdCounter++,
        text: this.newMessage,
        sender: 'user',
      };
      this.messages.push(userMessage);
      this.isLoading = true;

      try {
        // Enviar la tarea al backend
        const response = await api.post('/delegate', {
          query: this.newMessage,
          // Aquí se podría añadir más contexto si fuera necesario
        });
        
        const agentMessage = {
          id: this.messageIdCounter++,
          text: this.formatResponse(response.data),
          sender: 'agent',
        };
        this.messages.push(agentMessage);
      } catch (error) {
        const errorMessage = {
          id: this.messageIdCounter++,
          text: 'Error al contactar al agente. Inténtalo de nuevo.',
          sender: 'agent',
        };
        this.messages.push(errorMessage);
        console.error('Error al delegar tarea:', error);
      } finally {
        this.newMessage = '';
        this.isLoading = false;
      }
    },
    formatResponse(data) {
      // Formatea la respuesta del agente para mostrarla.
      // Puede ser un string o un objeto JSON.
      if (typeof data === 'object') {
        return JSON.stringify(data, null, 2);
      }
      return data;
    }
  },
  mounted() {
    if (this.initialPrompt) {
      this.messages.push({
        id: this.messageIdCounter++,
        text: this.initialPrompt,
        sender: 'agent',
      });
    }
  }
};
</script>

<style scoped>
.agent-interaction-container {
  max-height: 80vh;
}
</style>
