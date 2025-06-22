import { defineStore } from 'pinia';
import api from '../services/api';

export const useAgentStore = defineStore('agent', {
  state: () => ({
    messages: [],
    isLoading: false,
    error: null,
  }),
  actions: {
    async delegateTask(query, inputData = {}) {
      this.isLoading = true;
      this.error = null;
      this.messages.push({ author: 'user', content: query });

      try {
        const response = await api.delegateTask(query, inputData);
        this.messages.push({ author: 'agent', content: response.data.result });
      } catch (error) {
        this.error = error.response?.data?.error || 'Ocurrió un error al contactar al agente.';
        this.messages.push({ author: 'agent', content: this.error, isError: true });
      } finally {
        this.isLoading = false;
      }
    },
  },
}); 