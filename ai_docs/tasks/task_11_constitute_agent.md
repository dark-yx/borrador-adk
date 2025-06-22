# ✏️ Tarea 11: Implementación del Agente de Constitución de Empresas (ConstituteAgent)

**Objetivo:** Crear el `ConstituteAgent`, un agente conversacional que guía a los usuarios a través del proceso de constitución de una empresa, recopilando la información necesaria paso a paso.

## Instrucciones detalladas:
1.  **Crear el archivo del agente**: En `manager/sub_agents/constitute_agent/agent.py`, crear la clase `ConstituteAgent` que herede de `BaseAgent`.
2.  **Diseñar el flujo conversacional**: Definir los pasos y preguntas que el agente debe seguir para recolectar la información, como:
    -   Tipo de sociedad (ej. S.A.S., LLC).
    -   Nombre de la empresa.
    -   Información de los socios.
    -   Capital social.
    -   Objeto social.
3.  **Implementar la lógica de estado**: El agente debe mantener el estado de la conversación para saber qué información ya ha sido recolectada y cuál es la siguiente pregunta a realizar.
4.  **Generar un resumen**: Una vez que toda la información ha sido recopilada, el agente debe generar un resumen estructurado (ej. en JSON) con todos los datos, que podría ser utilizado por el `DocumentAgent` para redactar los estatutos.

## Archivos y módulos involucrados:
-   `legislink-pro/manager/sub_agents/constitute_agent/agent.py` (nuevo archivo)
-   `legislink-pro/manager/sub_agents/constitute_agent/__init__.py`

## Dependencias:
-   `task_07_adk_base_agent.md`

✅ **Criterio de completitud:** El `ConstituteAgent` puede mantener una conversación coherente con un usuario, hacer las preguntas necesarias para la constitución de una empresa y, al final, producir un resumen completo con la información recolectada. 