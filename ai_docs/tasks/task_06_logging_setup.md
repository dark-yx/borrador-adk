# ✏️ Tarea 6: Configuración del Sistema de Logging

**Objetivo:** Implementar un sistema de logging centralizado y configurable para registrar eventos importantes, errores y actividades de los agentes en la aplicación.

## Instrucciones detalladas:
1.  **Configurar el logging de Python**: En `config/logging.py`, utilizar el módulo `logging.config` de Python para configurar el sistema de logs.
2.  **Definir handlers**: Configurar al menos dos `handlers`:
    -   Un `StreamHandler` para mostrar logs en la consola durante el desarrollo.
    -   Un `RotatingFileHandler` para guardar los logs en archivos en el directorio `logs/`, con rotación por tamaño o tiempo para evitar archivos demasiado grandes.
3.  **Definir formato de log**: Crear un `Formatter` para estandarizar el formato de los mensajes de log (ej: `[%(asctime)s] %(levelname)s in %(module)s: %(message)s`).
4.  **Cargar la configuración**: En `api/main.py`, llamar a la función de configuración del logging al iniciar la aplicación para que esté disponible en todos los módulos.
5.  **Añadir logs de ejemplo**: En diferentes partes de la aplicación (ej. al iniciar, en la ruta de prueba), añadir llamadas al logger para registrar mensajes de diferentes niveles (`INFO`, `DEBUG`, `ERROR`).

## Archivos y módulos involucrados:
-   `legislink-pro/config/logging.py`
-   `legislink-pro/api/main.py`
-   `logs/` (directorio de salida)

## Dependencias:
-   `task_01_project_structure.md`

✅ **Criterio de completitud:** La aplicación genera logs tanto en la consola como en un archivo dentro del directorio `logs/`. Los logs tienen un formato consistente y son útiles para depurar y monitorear la aplicación. 