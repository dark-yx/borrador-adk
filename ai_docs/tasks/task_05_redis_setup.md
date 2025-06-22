# ✏️ Tarea 5: Configuración de Redis

**Objetivo:** Configurar e integrar Redis en la aplicación Flask para ser utilizado como caché y para la gestión de sesiones de los agentes.

## Instrucciones detalladas:
1.  **Instalar dependencias**: Añadir la librería `redis` de Python a `requirements.txt`.
2.  **Configurar la conexión**: En `config/settings.py`, obtener las variables de entorno `REDIS_HOST`, `REDIS_PORT` y `REDIS_DB`.
3.  **Crear un cliente de Redis**: En un nuevo archivo `services/cache.py` (o similar), crear una función o un singleton que inicialice y devuelva un cliente de Redis (`redis.Redis`).
4.  **Probar la conexión**: Añadir un pequeño script o una ruta de prueba en Flask que intente establecer un valor en Redis y luego leerlo para confirmar que la conexión es exitosa. Por ejemplo: `redis_client.set('test_key', 'hello_redis')` y luego `redis_client.get('test_key')`.

## Archivos y módulos involucrados:
-   `legislink-pro/services/cache.py` (nuevo archivo)
-   `legislink-pro/config/settings.py`
-   `legislink-pro/requirements.txt`
-   `legislink-pro/api/main.py` (para la ruta de prueba)

## Dependencias:
-   `task_02_environment_setup.md`

✅ **Criterio de completitud:** La aplicación Flask puede conectarse a Redis, y es capaz de escribir y leer datos. El cliente de Redis está disponible para ser utilizado por otros servicios o agentes en la aplicación. 