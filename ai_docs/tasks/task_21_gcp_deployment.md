# ✏️ Tarea 20: Despliegue en Google Cloud Platform (GCP)

**Objetivo:** Desplegar la aplicación contenedorizada en Google Cloud Platform, utilizando servicios gestionados como Cloud Run para el backend, Cloud SQL para la base de datos y MemoryStore para Redis.

## Instrucciones detalladas:
1.  **Configurar Cloud SQL**:
    -   Crear una instancia de Cloud SQL para MySQL en GCP.
    -   Configurar la base de datos, el usuario y la contraseña.
    -   Asegurarse de que las conexiones desde Cloud Run estarán permitidas.
2.  **Configurar MemoryStore**:
    -   Crear una instancia de MemoryStore para Redis.
    -   Configurar el acceso a través de un conector de VPC sin servidor para que Cloud Run pueda conectarse.
3.  **Subir imágenes a Google Artifact Registry**:
    -   Configurar Docker para autenticarse con Artifact Registry.
    -   Construir las imágenes de Docker del backend y el frontend.
    -   Etiquetar las imágenes y subirlas al Artifact Registry de tu proyecto de GCP.
4.  **Desplegar en Cloud Run**:
    -   Crear un nuevo servicio de Cloud Run para el backend, utilizando la imagen subida al Artifact Registry. Configurar las variables de entorno para conectarse a Cloud SQL y MemoryStore.
    -   Crear otro servicio de Cloud Run para el frontend (o usar un bucket de Cloud Storage con un balanceador de carga) para servir la interfaz de usuario.
5.  **Configurar CI/CD (Opcional)**:
    -   Crear un pipeline de CI/CD utilizando Cloud Build y GitHub Actions para automatizar el proceso de construcción y despliegue cada vez que se hace un push a la rama principal.

## Archivos y módulos involucrados:
-   `cloudbuild.yaml` (para la configuración de Cloud Build)
-   `.github/workflows/deploy.yml` (para GitHub Actions)
-   Archivos de configuración de despliegue en el directorio `deployment/`.

## Dependencias:
-   `task_19_dockerization.md`

✅ **Criterio de completitud:** La aplicación LegisLink Pro está desplegada y accesible públicamente a través de las URLs de Cloud Run. La aplicación es completamente funcional en el entorno de producción de GCP, conectándose correctamente a la base de datos y a la caché. 