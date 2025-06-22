# ✏️ Tarea 18: Integración con Google Calendar

**Objetivo:** Permitir que los agentes puedan crear y consultar eventos en el calendario de Google del usuario, para agendar reuniones, recordatorios o fechas límite de procesos legales.

## Instrucciones detalladas:
1.  **Configurar la API de Google Calendar**: En la consola de Google Cloud, habilitar la API de Google Calendar y usar las mismas credenciales de OAuth 2.0 de la tarea anterior (asegurándose de añadir el *scope* de Calendar).
2.  **Añadir el scope de Calendar**: Al implementar el flujo de autenticación de OAuth 2.0, añadir el scope `https://www.googleapis.com/auth/calendar` para solicitar los permisos necesarios.
3.  **Crear herramientas de Google Calendar**: En `services/google_apis.py`, desarrollar funciones para interactuar con la API de Calendar, como:
    -   `create_calendar_event(summary, start_time, end_time, attendees)`
    -   `list_upcoming_events(max_results)`
4.  **Crear un agente o modificar uno existente**: Se podría crear un `CalendarAgent` o añadir la funcionalidad a un agente más general para que pueda interpretar solicitudes como "Agenda una reunión con el cliente X para mañana a las 10 am".
5.  **Llamar a las herramientas**: El agente debe ser capaz de extraer los detalles del evento desde el lenguaje natural y llamar a la herramienta `create_calendar_event` con los parámetros correctos.

## Archivos y módulos involucrados:
-   `legislink-pro/services/google_apis.py`
-   `legislink-pro/manager/sub_agents/` (un agente nuevo o modificado)

## Dependencias:
-   `task_17_google_drive_integration.md` (para el flujo de autenticación OAuth 2.0)

✅ **Criterio de completitud:** Un usuario puede pedirle a la plataforma "crea un evento para discutir el caso Y el viernes a las 3 pm" y un nuevo evento aparece correctamente en su Google Calendar, con los detalles especificados. 