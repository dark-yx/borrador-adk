# ✏️ Tarea 14: Creación de Endpoints de API para Agentes

**Objetivo:** Exponer la funcionalidad del `AgentManager` a través de una API RESTful en Flask, permitiendo que un cliente (como el frontend de Vue.js) interactúe con el sistema de agentes.

## Instrucciones detalladas:
1.  **Crear un Blueprint de API**: En un nuevo archivo `api/routes.py`, crear un `Blueprint` de Flask para organizar las rutas relacionadas con los agentes.
2.  **Definir el endpoint de delegación**: Crear una ruta, por ejemplo `/api/v1/delegate`, que acepte peticiones `POST`.
3.  **Manejar la petición**: El endpoint debe:
    -   Recibir un JSON con la tarea o pregunta del usuario (ej. `{"query": "Redacta un NDA"}`).
    -   Instanciar (o recuperar una instancia singleton) del `AgentManager`.
    -   Llamar al método `delegate_task` del manager con la consulta del usuario.
    -   Recibir la respuesta del manager.
4.  **Devolver la respuesta**: Devolver la respuesta del agente como un JSON al cliente. Manejar posibles errores y devolver códigos de estado HTTP apropiados.
5.  **Registrar el Blueprint**: Registrar el `Blueprint` en la aplicación principal de Flask en `api/main.py`.

## Archivos y módulos involucrados:
-   `legislink-pro/api/routes.py` (nuevo archivo)
-   `legislink-pro/api/main.py`
-   `legislink-pro/manager/agent_manager.py`

## Dependencias:
-   `task_08_agent_manager.md`
-   Todos los agentes que se quieran exponer (Tareas 9-12).

✅ **Criterio de completitud:** Se puede realizar una petición `POST` a `/api/v1/delegate` con una tarea en formato JSON, y la API responde correctamente con el resultado generado por el `AgentManager` y el sub-agente correspondiente. 