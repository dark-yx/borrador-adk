# ✏️ Tarea 7: Estructura Base de Agentes con ADK

**Objetivo:** Definir una clase base para todos los sub-agentes utilizando el framework ADK, estableciendo una estructura común para la inicialización, ejecución y manejo de estado.

## Instrucciones detalladas:
1.  **Instalar ADK**: Añadir `adk` a `requirements.txt` si aún no está presente.
2.  **Crear una clase base**: En `manager/sub_agents/base_agent.py` (crear este archivo), definir una clase abstracta o una clase base llamada `BaseAgent`.
3.  **Definir la interfaz común**: La clase `BaseAgent` debe incluir:
    -   Un método `__init__` que reciba configuración, como el modelo de lenguaje (LLM) a utilizar.
    -   Un método abstracto `run` o `execute` que tomará un input (ej. un diccionario o un objeto de datos) y devolverá un resultado.
    -   Propiedades para gestionar el estado del agente y su historial de conversación, posiblemente utilizando el gestor de sesiones de ADK.
4.  **Integrar con el LLM de Vertex AI**: La clase base debe estar preparada para recibir una instancia de un modelo de lenguaje de Vertex AI (que se configurará más adelante) y pasarlo a los agentes.

## Archivos y módulos involucrados:
-   `legislink-pro/manager/sub_agents/base_agent.py` (nuevo archivo)
-   `legislink-pro/requirements.txt`

## Dependencias:
-   `task_01_project_structure.md`

✅ **Criterio de completitud:** Existe una clase `BaseAgent` que puede ser heredada por todos los sub-agentes. La clase define una estructura clara y obliga a implementar los métodos necesarios para la ejecución de tareas. 