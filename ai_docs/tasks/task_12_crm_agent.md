# ✏️ Tarea 12: Implementación del Agente de CRM (CRMAgent)

**Objetivo:** Desarrollar el `CRMAgent`, un agente capaz de interactuar con la base de datos de clientes (MySQL) para registrar, actualizar o consultar información de contactos y casos legales.

## Instrucciones detalladas:
1.  **Crear el archivo del agente**: En `manager/sub_agents/crm_agent/agent.py`, crear la clase `CRMAgent` que herede de `BaseAgent`.
2.  **Definir modelos de base de datos**: Asegurarse de que los modelos de `SQLAlchemy` para Clientes (`Customer`), Casos (`Case`), etc., están definidos.
3.  **Implementar funciones de base de datos**: Crear funciones para las operaciones CRUD (Crear, Leer, Actualizar, Borrar) sobre los modelos. Estas funciones deben manejar la sesión de la base de datos.
4.  **Desarrollar herramientas para el agente**: Exponer las funciones CRUD como herramientas (`tools`) que el agente pueda utilizar. Por ejemplo, `add_new_client`, `get_client_details`, `update_case_status`.
5.  **Implementar el método `run`**: El método `run` del agente interpretará el lenguaje natural del usuario (ej. "Añadir a Juan Pérez como nuevo cliente") y llamará a la herramienta apropiada con los parámetros correctos.

## Archivos y módulos involucrados:
-   `legislink-pro/manager/sub_agents/crm_agent/agent.py` (nuevo archivo)
-   `legislink-pro/manager/sub_agents/crm_agent/tools.py` (opcional)
-   `legislink-pro/models/` (donde residen los modelos de DB)
-   `legislink-pro/services/database.py`

## Dependencias:
-   `task_04_database_setup.md`
-   `task_07_adk_base_agent.md`

✅ **Criterio de completitud:** El `CRMAgent` puede procesar una solicitud en lenguaje natural para gestionar datos de clientes o casos, y la base de datos refleja los cambios correctamente. Por ejemplo, al pedir "buscar el caso 123", el agente devuelve la información correcta de la base de datos. 