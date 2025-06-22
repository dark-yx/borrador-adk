# ✏️ Tarea 1: Configuración de la Estructura del Proyecto

**Objetivo:** Crear la estructura de directorios y archivos inicial para la plataforma LegisLink Pro, asegurando una base organizada para el desarrollo.

## Instrucciones detalladas:
1.  Crear los directorios principales: `legislink-pro`, `api`, `config`, `deployment`, `frontend`, `logs`, `manager`, `services`, `static`, `templates`, `tests`.
2.  Dentro de `manager`, crear el directorio `sub_agents`.
3.  Dentro de `sub_agents`, crear los directorios para cada agente: `constitute_agent`, `crm_agent`, `document_agent`, `rag_agent`.
4.  Crear archivos `__init__.py` en todos los directorios y subdirectorios de la aplicación para que Python los reconozca como paquetes.
5.  Crear los archivos iniciales vacíos:
    -   `legislink-pro/requirements.txt`
    -   `legislink-pro/env.example`
    -   `legislink-pro/config/settings.py`
    -   `legislink-pro/config/logging.py`
    -   `legislink-pro/services/database.py`
    -   `legislink-pro/services/google_apis.py`
    -   `legislink-pro/api/main.py` (o como se decida llamar al entrypoint)

## Archivos y módulos involucrados:
-   Toda la estructura de directorios bajo `legislink-pro/`.
-   `legislink-pro/requirements.txt`
-   `legislink-pro/env.example`
-   `legislink-pro/config/settings.py`
-   `legislink-pro/config/logging.py`
-   `legislink-pro/services/database.py`
-   `legislink-pro/services/google_apis.py`
-   `legislink-pro/api/main.py`

## Dependencias:
-   Ninguna.

✅ **Criterio de completitud:** La estructura de directorios y archivos está creada según lo especificado, lista para que se añada el código en las siguientes tareas. 