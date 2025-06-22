# ✏️ Tarea 4: Configuración de la Base de Datos (MySQL)

**Objetivo:** Integrar y configurar una base de datos MySQL con la aplicación Flask utilizando una librería como `SQLAlchemy` para la gestión de modelos y sesiones.

## Instrucciones detalladas:
1.  **Instalar dependencias**: Añadir `Flask-SQLAlchemy` y `mysqlclient` (o `PyMySQL`) a `requirements.txt`.
2.  **Configurar la conexión**: En `config/settings.py`, construir la URL de conexión a la base de datos (`SQLALCHEMY_DATABASE_URI`) utilizando las variables de entorno previamente definidas (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME).
3.  **Inicializar SQLAlchemy**: En `services/database.py`, inicializar SQLAlchemy con la aplicación Flask para crear un objeto `db` que será usado para definir modelos e interactuar con la base de datos.
4.  **Crear un modelo de ejemplo**: Definir un modelo de ejemplo (ej. `User` o `LegalCase`) en un nuevo directorio `models` para verificar que la conexión y el ORM funcionan.
5.  **Integrar con la app Flask**: Asegurarse de que la inicialización de la base de datos se llama en el `main.py` de la API.

## Archivos y módulos involucrados:
-   `legislink-pro/services/database.py`
-   `legislink-pro/config/settings.py`
-   `legislink-pro/requirements.txt`
-   `legislink-pro/models/` (nuevo directorio y archivos de modelos)
-   `legislink-pro/api/main.py`

## Dependencias:
-   `task_03_flask_setup.md`

✅ **Criterio de completitud:** La aplicación Flask se conecta exitosamente a la base de datos MySQL al iniciar. Las migraciones o la creación de tablas a partir de los modelos se pueden ejecutar sin errores. 