# ✏️ Tarea 15: Configuración Básica del Frontend (Vue.js)

**Objetivo:** Inicializar un proyecto de Vue.js y configurar la estructura básica para la interfaz de usuario de LegisLink Pro.

## Instrucciones detalladas:
1.  **Instalar Vue CLI**: Asegurarse de tener Vue CLI instalado (`npm install -g @vue/cli`).
2.  **Crear el proyecto Vue**: Dentro del directorio `legislink-pro/`, ejecutar `vue create frontend` para inicializar un nuevo proyecto de Vue.js. Se recomienda seleccionar Vue 3, Vue Router y Pinia (o Vuex) para el manejo de estado.
3.  **Limpiar el proyecto inicial**: Eliminar los componentes de ejemplo (como `HelloWorld.vue`) y limpiar `App.vue` para tener un lienzo en blanco.
4.  **Configurar la comunicación con el backend**: Instalar `axios` (`npm install axios`) para realizar peticiones HTTP al backend de Flask. Configurar una instancia de `axios` con la URL base de la API (ej. `http://localhost:5000/api/v1`).
5.  **Crear una vista principal**: Crear un componente principal (ej. `views/ChatView.vue`) que contendrá la interfaz de chat con los agentes.
6.  **Configurar el enrutador**: Configurar `vue-router` para que la vista de chat sea la ruta principal de la aplicación.

## Archivos y módulos involucrados:
-   `legislink-pro/frontend/` (todo el directorio)
-   `legislink-pro/frontend/src/App.vue`
-   `legislink-pro/frontend/src/router/index.js`
-   `legislink-pro/frontend/src/views/ChatView.vue` (nuevo archivo)
-   `legislink-pro/frontend/src/services/api.js` (para la configuración de axios)

## Dependencias:
-   `task_14_api_endpoints.md`

✅ **Criterio de completitud:** El proyecto de Vue.js se puede iniciar (`npm run serve`) y muestra una página en blanco o una estructura básica sin errores. La configuración de `axios` está lista para comunicarse con el backend de Flask. 