<template>
  <div class="document-generation">
    <div class="header mb-6">
      <h1 class="text-3xl font-bold mb-2">{{ $t('document_generation.title') }}</h1>
      <p class="text-gray-400">{{ $t('document_generation.subtitle', 'Genera documentos legales profesionales con IA') }}</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Panel de Generación -->
      <div class="bg-gray-800 p-6 rounded-lg">
        <h2 class="text-xl font-semibold mb-4">{{ $t('document_generation.generation_panel', 'Generar Documento') }}</h2>
        
        <form @submit.prevent="generateDocument" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">{{ $t('document_generation.document_type', 'Tipo de Documento') }}</label>
            <select v-model="documentForm.type" class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white">
              <option value="contrato">{{ $t('document_generation.contract', 'Contrato') }}</option>
              <option value="acuerdo">{{ $t('document_generation.agreement', 'Acuerdo') }}</option>
              <option value="poder">{{ $t('document_generation.power_of_attorney', 'Poder') }}</option>
              <option value="testamento">{{ $t('document_generation.will', 'Testamento') }}</option>
              <option value="demanda">{{ $t('document_generation.lawsuit', 'Demanda') }}</option>
              <option value="otro">{{ $t('document_generation.other', 'Otro') }}</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">{{ $t('document_generation.description', 'Descripción') }}</label>
            <textarea 
              v-model="documentForm.description" 
              rows="3"
              :placeholder="$t('document_generation.description_placeholder', 'Describe el documento que necesitas...')"
              class="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white resize-none"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">{{ $t('document_generation.key_points', 'Puntos Clave') }}</label>
            <div class="space-y-2">
              <div v-for="(point, index) in documentForm.points" :key="index" class="flex gap-2">
                <input 
                  v-model="documentForm.points[index]" 
                  :placeholder="$t('document_generation.point_placeholder', 'Punto clave...')"
                  class="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
                />
                <button 
                  @click="removePoint(index)" 
                  type="button"
                  class="px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg"
                >
                  ×
                </button>
              </div>
              <button 
                @click="addPoint" 
                type="button"
                class="text-blue-400 hover:text-blue-300 text-sm"
              >
                + {{ $t('document_generation.add_point', 'Añadir punto') }}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="isGenerating"
            class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 px-4 rounded-lg"
          >
            <span v-if="isGenerating">{{ $t('document_generation.generating', 'Generando...') }}</span>
            <span v-else>{{ $t('document_generation.generate', 'Generar Documento') }}</span>
          </button>
        </form>
      </div>

      <!-- Panel de Chat/Resultado -->
      <div class="bg-gray-800 p-6 rounded-lg">
        <h2 class="text-xl font-semibold mb-4">{{ $t('document_generation.result', 'Resultado') }}</h2>
        
        <div class="h-96 overflow-y-auto bg-gray-900 rounded-lg p-4 mb-4">
          <div v-if="messages.length === 0" class="text-gray-400 text-center py-8">
            {{ $t('document_generation.no_messages', 'No hay mensajes aún. Genera un documento para comenzar.') }}
          </div>
          
          <div v-for="message in messages" :key="message.id" class="mb-4">
            <div :class="message.sender === 'user' ? 'text-right' : 'text-left'">
              <div :class="message.sender === 'user' ? 'bg-blue-600' : 'bg-gray-700'" 
                   class="inline-block p-3 rounded-lg max-w-xs lg:max-w-md">
                <div v-if="message.sender === 'agent' && message.document" class="space-y-2">
                  <div class="font-semibold">{{ $t('document_generation.document_generated', 'Documento Generado') }}</div>
                  <div class="text-sm bg-gray-800 p-2 rounded border-l-4 border-green-500">
                    <pre class="whitespace-pre-wrap text-xs">{{ message.document }}</pre>
                  </div>
                  <div v-if="message.driveLink" class="text-xs text-green-400">
                    {{ $t('document_generation.saved_to_drive', 'Guardado en Google Drive') }}
                  </div>
                </div>
                <div v-else>
                  {{ message.text }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentDocument" class="space-y-2">
          <button 
            @click="downloadDocument" 
            class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg"
          >
            {{ $t('document_generation.download', 'Descargar Documento') }}
          </button>
          <button 
            @click="reviewDocument" 
            class="w-full bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded-lg"
          >
            {{ $t('document_generation.review', 'Revisar Documento') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'DocumentGenerationView',
  data() {
    return {
      documentForm: {
        type: 'contrato',
        description: '',
        points: ['']
      },
      messages: [],
      currentDocument: null,
      isGenerating: false,
      messageIdCounter: 0
    };
  },
  methods: {
    addPoint() {
      this.documentForm.points.push('');
    },
    removePoint(index) {
      if (this.documentForm.points.length > 1) {
        this.documentForm.points.splice(index, 1);
      }
    },
    async generateDocument() {
      if (!this.documentForm.description.trim()) {
        this.addMessage('Por favor, proporciona una descripción del documento.', 'agent');
        return;
      }

      this.isGenerating = true;
      
      // Añadir mensaje del usuario
      this.addMessage(`Generar ${this.documentForm.type}: ${this.documentForm.description}`, 'user');

      try {
        const response = await api.delegateTask('generar documento', {
          tipo: this.documentForm.type,
          descripcion: this.documentForm.description,
          puntos: this.documentForm.points.filter(p => p.trim())
        });

        if (response.data.result && response.data.result.documento_generado) {
          this.currentDocument = response.data.result.documento_generado;
          this.addMessage({
            text: 'Documento generado exitosamente',
            document: this.currentDocument,
            driveLink: response.data.result.google_drive_resultado
          }, 'agent');
        } else {
          this.addMessage('Error al generar el documento. Inténtalo de nuevo.', 'agent');
        }
      } catch (error) {
        console.error('Error:', error);
        this.addMessage('Error al generar el documento. Inténtalo de nuevo.', 'agent');
      } finally {
        this.isGenerating = false;
      }
    },
    addMessage(content, sender) {
      const message = {
        id: this.messageIdCounter++,
        sender,
        text: typeof content === 'string' ? content : content.text,
        document: content.document,
        driveLink: content.driveLink
      };
      this.messages.push(message);
    },
    downloadDocument() {
      if (!this.currentDocument) return;
      
      const blob = new Blob([this.currentDocument], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${this.documentForm.type}_${new Date().toISOString().split('T')[0]}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    },
    async reviewDocument() {
      if (!this.currentDocument) return;
      
      this.addMessage('Revisando documento...', 'user');
      
      try {
        const response = await api.delegateTask('revisar documento', {
          documento: this.currentDocument,
          tipo_revision: 'general'
        });

        if (response.data.result && response.data.result.documento_revisado) {
          this.addMessage({
            text: 'Documento revisado',
            document: response.data.result.documento_revisado
          }, 'agent');
        } else {
          this.addMessage('Error al revisar el documento.', 'agent');
        }
      } catch (error) {
        console.error('Error:', error);
        this.addMessage('Error al revisar el documento.', 'agent');
      }
    }
  }
};
</script> 