# ✏️ Tarea 9: Implementación del Agente de Documentos (DocumentAgent)

**Objetivo:** Crear el `DocumentAgent`, un agente especializado en la creación, redacción y modificación de documentos legales básicos.

## Instrucciones detalladas:
1.  **Crear el archivo del agente**: En `manager/sub_agents/document_agent/agent.py`, crear la clase `DocumentAgent` que herede de `BaseAgent`.
2.  **Definir el prompt del sistema**: Crear un prompt de sistema (`system_prompt`) que instruya al modelo de lenguaje sobre su rol: "Eres un asistente legal experto en la redacción de documentos. Tu tarea es generar, revisar o modificar documentos legales según las especificaciones del usuario".
3.  **Implementar el método `run`**: El método `run` recibirá una descripción de la tarea (ej. "Redacta un contrato de confidencialidad simple") y utilizará el LLM para generar el contenido del documento.
4.  **Definir la estructura de entrada/salida**: La entrada debe especificar el tipo de documento y los puntos clave a incluir. La salida debe ser el texto del documento generado.
5.  **Añadir herramientas (opcional)**: Si el agente necesita funcionalidades adicionales (como guardar el documento), se pueden definir herramientas (`tools`) específicas para él.

## Archivos y módulos involucrados:
-   `legislink-pro/manager/sub_agents/document_agent/agent.py` (nuevo archivo)
-   `legislink-pro/manager/sub_agents/document_agent/__init__.py`
-   `legislink-pro/manager/agent_manager.py` (para integrar el nuevo agente)

## Dependencias:
-   `task_07_adk_base_agent.md`

✅ **Criterio de completitud:** El `DocumentAgent` puede recibir una solicitud para crear un documento simple y devuelve un borrador de texto coherente y relevante para la solicitud. El `AgentManager` puede delegarle tareas. 