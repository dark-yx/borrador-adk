# ✏️ Tarea 17: Integración con Google Drive

**Objetivo:** Implementar la capacidad de guardar y leer documentos desde Google Drive, permitiendo que agentes como el `DocumentAgent` interactúen con los archivos del usuario de forma segura.

## Instrucciones detalladas:
1.  **Configurar la API de Google Drive**: En la consola de Google Cloud, habilitar la API de Google Drive y crear credenciales de OAuth 2.0.
2.  **Instalar la librería cliente**: Añadir `google-api-python-client` y `google-auth-httplib2` a `requirements.txt`.
3.  **Implementar el flujo de autenticación**: En `services/google_apis.py`, implementar el flujo de OAuth 2.0 para que un usuario pueda autorizar a la aplicación a acceder a su Google Drive. Los tokens de acceso deben guardarse de forma segura, asociados al usuario.
4.  **Crear herramientas de Google Drive**: Desarrollar funciones que actúen como herramientas para los agentes, como:
    -   `upload_file_to_drive(file_content, file_name, folder_id)`
    -   `list_files_in_folder(folder_id)`
    -   `read_file_from_drive(file_id)`
5.  **Integrar con `DocumentAgent`**: Modificar el `DocumentAgent` para que, después de generar un documento, pueda usar la herramienta `upload_file_to_drive` para guardarlo en la cuenta del usuario.

## Archivos y módulos involucrados:
-   `legislink-pro/services/google_apis.py`
-   `legislink-pro/requirements.txt`
-   `legislink-pro/manager/sub_agents/document_agent/agent.py`

## Dependencias:
-   `task_09_document_agent.md`
-   Configuración de un proyecto en Google Cloud.

✅ **Criterio de completitud:** El `DocumentAgent` (o cualquier otro agente con permisos) puede guardar un documento generado en el Google Drive de un usuario que haya completado el flujo de autenticación. El archivo aparece correctamente en la cuenta de Drive del usuario. 