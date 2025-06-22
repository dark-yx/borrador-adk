# ✏️ Tarea 16: Implementación de la Interfaz de Usuario para Interacción con Agentes

**Objetivo:** Desarrollar una interfaz de chat en Vue.js que permita a los usuarios enviar consultas al backend y visualizar las respuestas de los agentes de forma clara e interactiva.

## Instrucciones detalladas:
1.  **Diseñar el componente de chat**: En `views/ChatView.vue`, crear la estructura de la interfaz, que debe incluir:
    -   Un área de visualización de mensajes (historial de chat).
    -   Un campo de entrada de texto (`<input>` o `<textarea>`) para que el usuario escriba su consulta.
    -   Un botón de envío.
2.  **Manejar el estado del chat**: Utilizar Pinia o el sistema de estado de Vue para gestionar:
    -   La lista de mensajes (tanto del usuario como del agente).
    -   El estado de carga (para mostrar un indicador mientras el agente procesa la solicitud).
3.  **Implementar la lógica de envío**:
    -   Al hacer clic en el botón de envío, tomar el texto del input.
    -   Llamar a la función del servicio `api.js` que realiza la petición `POST` al endpoint `/api/v1/delegate`.
    -   Añadir el mensaje del usuario al historial de chat.
4.  **Mostrar la respuesta del agente**:
    -   Cuando la petición a la API tiene éxito, añadir la respuesta del agente al historial de chat.
    -   Manejar los errores de la API y mostrar un mensaje de error al usuario si es necesario.
5.  **Estilizar la interfaz**: Aplicar CSS o un framework de componentes como Vuetify o Tailwind CSS para que la interfaz sea atractiva y fácil de usar.

## Archivos y módulos involucrados:
-   `legislink-pro/frontend/src/views/ChatView.vue`
-   `legislink-pro/frontend/src/components/ChatMessage.vue` (componente para mostrar un mensaje individual)
-   `legislink-pro/frontend/src/services/api.js`
-   `legislink-pro/frontend/src/store/chat.js` (archivo de estado de Pinia/Vuex)

## Dependencias:
-   `task_15_vue_frontend_setup.md`

✅ **Criterio de completitud:** Un usuario puede escribir una consulta en la interfaz de chat, enviarla al backend, y ver tanto su mensaje como la respuesta del agente mostrados en el historial del chat. La comunicación entre el frontend y el backend es funcional. 