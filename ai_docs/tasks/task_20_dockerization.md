# ✏️ Tarea 19: Dockerización de la Aplicación

**Objetivo:** Crear archivos `Dockerfile` y `docker-compose.yml` para contenedorizar los diferentes servicios de la aplicación (backend de Flask, frontend de Vue.js, MySQL, Redis), facilitando el desarrollo y el despliegue.

## Instrucciones detalladas:
1.  **Crear un `Dockerfile` para el backend**:
    -   En el directorio `legislink-pro/`, crear un `Dockerfile` para la aplicación Flask.
    -   Usar una imagen base de Python (ej. `python:3.10-slim`).
    -   Copiar `requirements.txt` e instalar las dependencias.
    -   Copiar el resto del código de la aplicación.
    -   Exponer el puerto que usa Flask (ej. `5000`) y definir el `CMD` para iniciar la aplicación (ej. `gunicorn -w 4 'api.main:app'`).
2.  **Crear un `Dockerfile` para el frontend**:
    -   En `legislink-pro/frontend/`, crear un `Dockerfile` para la aplicación Vue.js.
    -   Utilizar un enfoque de "multi-stage build":
        -   Una primera etapa (`build stage`) con una imagen de `node` para instalar dependencias y construir los archivos estáticos (`npm run build`).
        -   Una segunda etapa con una imagen de `nginx` para servir los archivos estáticos generados en la etapa anterior.
3.  **Crear `docker-compose.yml`**:
    -   En la raíz del proyecto, crear un archivo `docker-compose.yml`.
    -   Definir los servicios: `backend`, `frontend`, `db` (usando la imagen oficial de `mysql`), y `cache` (usando la imagen de `redis`).
    -   Configurar las redes, volúmenes (para la persistencia de datos de MySQL) y variables de entorno para cada servicio.

## Archivos y módulos involucrados:
-   `legislink-pro/Dockerfile` (para el backend)
-   `legislink-pro/frontend/Dockerfile` (para el frontend)
-   `docker-compose.yml` (en la raíz)
-   `.dockerignore` (para excluir archivos innecesarios de los contenedores)

## Dependencias:
-   Todas las tareas anteriores, ya que la aplicación debe ser funcional antes de ser contenedorizada.

✅ **Criterio de completitud:** Al ejecutar `docker-compose up` desde la raíz del proyecto, todos los servicios (backend, frontend, db, cache) se inician correctamente y pueden comunicarse entre sí. La aplicación es completamente funcional dentro del entorno de Docker. 