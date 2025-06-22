# ✏️ Tarea 10: Implementación del Agente de Búsqueda y Aumentación (RAGAgent)

**Objetivo:** Desarrollar el `RAGAgent`, un agente que utiliza la técnica RAG (Retrieval-Augmented Generation) para responder preguntas basándose en una base de conocimiento de documentos legales (ej. leyes, jurisprudencia).

## Instrucciones detalladas:
1.  **Configurar Vertex AI Search/Vector Search**: La implementación de RAG requiere una base de datos vectorial. Esta tarea implica configurar el servicio correspondiente en Google Cloud.
2.  **Crear el archivo del agente**: En `manager/sub_agents/rag_agent/agent.py`, crear la clase `RAGAgent` que herede de `BaseAgent`.
3.  **Implementar la lógica de recuperación**: El agente debe ser capaz de:
    -   Tomar una pregunta del usuario.
    -   Convertir la pregunta en un embedding vectorial.
    -   Consultar la base de datos vectorial para encontrar los documentos más relevantes.
4.  **Implementar la lógica de generación aumentada**:
    -   Construir un prompt que incluya la pregunta original y el contexto recuperado de los documentos.
    -   Enviar este prompt al LLM para generar una respuesta informada.
5.  **Crear herramientas de ingesta**: Desarrollar scripts o herramientas para cargar y procesar documentos en la base de datos vectorial (ej. un script que lea PDFs de una carpeta, los divida en trozos y los indexe).

## Archivos y módulos involucrados:
-   `legislink-pro/manager/sub_agents/rag_agent/agent.py` (nuevo archivo)
-   `legislink-pro/manager/sub_agents/rag_agent/tools/` (para scripts de ingesta)
-   `legislink-pro/services/google_apis.py` (para interactuar con Vertex AI Search)

## Dependencias:
-   `task_07_adk_base_agent.md`
-   Una configuración funcional de Google Cloud / Vertex AI.

✅ **Criterio de completitud:** El `RAGAgent` puede responder a una pregunta sobre un tema legal específico utilizando información extraída de su base de conocimiento, proporcionando respuestas más precisas y fundamentadas que si usara solo su conocimiento pre-entrenado. 