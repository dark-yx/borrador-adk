# ✏️ Tarea 8: Implementación del Gestor de Agentes (Agent Manager)

**Objetivo:** Crear el `AgentManager`, un componente central que orquesta la ejecución de los diferentes sub-agentes, gestionando el flujo de datos y la comunicación entre ellos.

## Instrucciones detalladas:
1.  **Crear el `AgentManager`**: En `manager/agent_manager.py` (crear este archivo), definir la clase `AgentManager`.
2.  **Inicializar sub-agentes**: El `AgentManager` debe importar e inicializar una instancia de cada sub-agente (que se crearán en tareas posteriores). Inicialmente, se pueden usar clases `mock` o placeholders.
3.  **Definir el método de orquestación**: Implementar un método principal, como `delegate_task(task_description)`, que reciba una descripción de la tarea y determine qué agente (o secuencia de agentes) es el más adecuado para manejarla.
4.  **Lógica de enrutamiento**: La lógica de enrutamiento puede ser simple al principio (basada en palabras clave) y luego evolucionar para usar un modelo de lenguaje que decida el mejor agente.
5.  **Gestionar el estado**: El `AgentManager` debe mantener el estado de la conversación o del flujo de trabajo, pasando el contexto relevante a cada sub-agente cuando es invocado.

## Archivos y módulos involucrados:
-   `legislink-pro/manager/agent_manager.py` (nuevo archivo)
-   `legislink-pro/manager/sub_agents/` (importará los agentes de este directorio)

## Dependencias:
-   `task_07_adk_base_agent.md`

✅ **Criterio de completitud:** El `AgentManager` puede ser instanciado y su método de delegación de tareas puede invocar (aunque sea de forma simulada) al sub-agente correcto basándose en una entrada de texto simple. 