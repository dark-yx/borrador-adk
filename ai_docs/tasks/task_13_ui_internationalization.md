# ✏️ Tarea 13: Internacionalización de la Interfaz de Usuario (i18n)

**Objetivo:** Implementar un sistema de internacionalización robusto en el frontend (Vue 3) para soportar múltiples idiomas y sincronizar la preferencia de idioma del usuario en toda la plataforma.

## Instrucciones detalladas:
1. **Instalar y configurar vue-i18n**: Añadir la librería `vue-i18n` al proyecto frontend y configurarla en el entrypoint principal.
2. **Estructura de archivos de recursos**: Crear archivos de recursos (JSON o YAML) para cada idioma soportado (ej: en, es, pt, fr) en un directorio `/frontend/locales/`.
3. **Selector de idioma**: Implementar un componente de selección de idioma visible y persistente (localStorage/cookie).
4. **Internacionalizar todos los textos**: Reemplazar todos los textos hardcodeados de la UI por claves i18n.
5. **Sincronización con backend y prompts**: Asegurarse de que el idioma seleccionado se incluya en los prompts enviados al backend para que el modelo de IA responda en el idioma correcto.
6. **Fallback y accesibilidad**: Configurar fallback a inglés y asegurar accesibilidad en todos los idiomas.

## Archivos y módulos involucrados:
- `/frontend/locales/`
- `/frontend/src/i18n.js` o `/frontend/src/i18n.ts`
- Componentes Vue principales (Navbar, Login, Dashboard, etc.)

## Dependencias:
- `task_15_vue_frontend_setup.md` (puede intercambiarse el orden si se prefiere implementar i18n antes del diseño visual)

✅ **Criterio de completitud:** Toda la interfaz de usuario es multilingüe, el usuario puede cambiar de idioma en cualquier momento y la preferencia se mantiene en la sesión. Los prompts enviados al backend incluyen el idioma seleccionado. 