# ✏️ Tarea 2: Configuración del Entorno de Desarrollo

**Objetivo:** Definir y documentar las variables de entorno necesarias para el funcionamiento de la aplicación, incluyendo credenciales de base de datos, APIs y configuraciones de Flask.

## Instrucciones detalladas:
1.  **Copiar `env.example` a `.env`**: Crear un archivo `.env` a partir de `env.example` para las configuraciones locales. Este archivo no debe ser versionado en Git.
2.  **Definir variables en `env.example`**: Añadir las siguientes variables al archivo `env.example` con valores por defecto o ejemplos:
    ```env
    # Flask
    FLASK_APP=api.main:app
    FLASK_ENV=development
    SECRET_KEY='una-clave-secreta-muy-segura'

    # MySQL Database
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=legislink
    DB_PASSWORD=password
    DB_NAME=legislink_db

    # Redis
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0

    # Google Cloud / Vertex AI
    GOOGLE_APPLICATION_CREDENTIALS='/path/to/your/credentials.json'
    GCP_PROJECT_ID='your-gcp-project-id'
    GCP_REGION='us-central1'
    ```
3.  **Cargar variables en la aplicación**: En `config/settings.py`, usar una librería como `python-dotenv` para cargar las variables del archivo `.env`.
4.  **Añadir `.env` a `.gitignore`**: Asegurarse de que el archivo `.env` esté incluido en el `.gitignore` del proyecto para evitar subir credenciales al repositorio.

## Archivos y módulos involucrados:
-   `legislink-pro/env.example`
-   `legislink-pro/.env` (local)
-   `legislink-pro/config/settings.py`
-   `.gitignore`

## Dependencias:
-   `task_01_project_structure.md`

✅ **Criterio de completitud:** La aplicación puede cargar todas las configuraciones necesarias desde las variables de entorno definidas en el archivo `.env`. El archivo `env.example` sirve como plantilla para nuevas configuraciones. 