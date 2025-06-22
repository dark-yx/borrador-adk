# ✏️ Tarea 3: Configuración Básica de la Aplicación Flask

**Objetivo:** Crear una instancia básica de la aplicación Flask que sirva como punto de entrada y configure las extensiones principales.

## Instrucciones detalladas:
1.  **Instalar dependencias**: Añadir `Flask`, `python-dotenv`, y `Flask-Cors` al archivo `requirements.txt`.
2.  **Crear la instancia de Flask**: En `api/main.py` (o como se haya nombrado al entrypoint), crear una instancia de la aplicación Flask.
3.  **Configurar la aplicación**:
    -   Importar las configuraciones desde `config/settings.py`.
    -   Inicializar `Flask-Cors` para permitir peticiones desde el frontend (Vue.js).
4.  **Crear una ruta de prueba**: Añadir una ruta raíz (`/` o `/api/health`) que devuelva un JSON de estado, como `{"status": "ok"}`, para verificar que la aplicación funciona correctamente.
5.  **Actualizar `settings.py`**: Asegurarse de que `config/settings.py` carga las variables de entorno utilizando `os.getenv()` o similar.

## Archivos y módulos involucrados:
-   `legislink-pro/api/main.py`
-   `legislink-pro/config/settings.py`
-   `legislink-pro/requirements.txt`

## Dependencias:
-   `task_01_project_structure.md`
-   `task_02_environment_setup.md`

✅ **Criterio de completitud:** Al ejecutar `flask run` (o el comando de inicio configurado), la aplicación Flask se inicia sin errores y la ruta de prueba (`/api/health`) devuelve una respuesta JSON exitosa. 