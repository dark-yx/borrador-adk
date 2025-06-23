# 📋 Resumen de Migración: LegisLink Pro → LegisLink AI

## 🎯 Cambios Principales

### Nombre del Proyecto
- **Antes**: `legislink-pro`
- **Después**: `legislink-ai`

### Nombre de la Aplicación
- **Antes**: `LegisLink Pro`
- **Después**: `LegisLink AI`

## 📁 Archivos que Cambian

### Archivos de Configuración
- `env.example`
- `README.md`
- `CONFIGURATION_GUIDE.md`
- `config/settings.py`
- `cloudbuild.yaml`
- `.github/workflows/deploy.yml`
- `docker-compose.yml` (en directorio padre)

### Scripts
- `scripts/setup_complete.py`
- `scripts/setup_vertex_ai.py`
- `scripts/setup_gemini.py`
- `scripts/setup_drive.py`
- `scripts/setup_secrets.py`
- `scripts/update_env.py`

### Frontend
- `frontend/package.json`
- `frontend/src/locales/en.json`
- `frontend/src/locales/es.json`

## 🔧 Servicios de Google Cloud

### Nuevos Recursos
- **Proyecto**: `legislink-ai`
- **Service Account**: `legislink-ai-service@legislink-ai.iam.gserviceaccount.com`
- **Cloud SQL**: `legislink-ai-db`
- **Base de datos**: `legislink_ai_db`
- **Usuario DB**: `legislink-ai`
- **MemoryStore**: `legislink-ai-redis`
- **Artifact Registry**: `legislink-ai-repo`
- **Cloud Run Backend**: `legislink-ai-backend`
- **Cloud Run Frontend**: `legislink-ai-frontend`

### Secrets
- `legislink-ai-gemini-key`
- `legislink-ai-db-password`
- `legislink-ai-db-host`
- `legislink-ai-db-name`
- `legislink-ai-db-user`
- `legislink-ai-drive-folder`

## 🚀 Proceso de Migración

### Opción 1: Automática (Recomendada)
```bash
# Ejecutar migración automática
python scripts/rename_project.py

# Verificar migración
python scripts/verify_migration.py
```

### Opción 2: Manual
1. Crear nuevo proyecto en Google Cloud
2. Habilitar APIs necesarias
3. Crear service account y asignar roles
4. Configurar servicios (Cloud SQL, MemoryStore, etc.)
5. Actualizar todos los archivos del proyecto
6. Renombrar directorio
7. Actualizar GitHub secrets

## 📝 Variables de Entorno Actualizadas

### Antes
```env
GCP_PROJECT_ID=legislink-pro
DB_HOST=legislink-db.legislink-pro.us-central1
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/legislink-service-key.json
DB_NAME=legislink_db
DB_USER=legislink
```

### Después
```env
GCP_PROJECT_ID=legislink-ai
DB_HOST=legislink-ai-db.legislink-ai.us-central1
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/legislink-ai-service-key.json
DB_NAME=legislink_ai_db
DB_USER=legislink-ai
```

## 🔗 URLs Actualizadas

### Google Cloud Console
- **Antes**: https://console.cloud.google.com/home/dashboard?project=legislink-pro
- **Después**: https://console.cloud.google.com/home/dashboard?project=legislink-ai

### Cloud Run
- **Antes**: https://legislink-backend-us-central1-legislink-pro.a.run.app
- **Después**: https://legislink-ai-backend-us-central1-legislink-ai.a.run.app

### APIs
- **Antes**: https://console.cloud.google.com/apis/dashboard?project=legislink-pro
- **Después**: https://console.cloud.google.com/apis/dashboard?project=legislink-ai

## 🐳 Docker

### Repositorio
- **Antes**: `us-central1-docker.pkg.dev/legislink-pro/legislink-repo`
- **Después**: `us-central1-docker.pkg.dev/legislink-ai/legislink-ai-repo`

### Imágenes
- **Antes**: `legislink-backend`, `legislink-frontend`
- **Después**: `legislink-ai-backend`, `legislink-ai-frontend`

## 🔄 GitHub Actions

### Secrets Actualizados
- `GCP_SA_KEY`: Nuevo archivo de credenciales
- `PROJECT_ID`: `legislink-ai`

### Workflow
- Actualiza referencias al proyecto
- Actualiza service account
- Actualiza nombres de servicios

## 📊 Checklist de Verificación

### ✅ Google Cloud
- [ ] Proyecto `legislink-ai` creado
- [ ] Facturación habilitada
- [ ] APIs habilitadas
- [ ] Service account configurado
- [ ] Cloud SQL configurado
- [ ] MemoryStore configurado
- [ ] Artifact Registry configurado
- [ ] Secret Manager configurado

### ✅ Archivos
- [ ] Todos los archivos actualizados
- [ ] Sin referencias al nombre anterior
- [ ] Configuraciones correctas

### ✅ Directorio
- [ ] Directorio renombrado
- [ ] Estructura correcta

### ✅ Despliegue
- [ ] GitHub secrets actualizados
- [ ] Aplicación desplegada
- [ ] Funcionamiento verificado

## 🛠️ Scripts Disponibles

### Migración
- `scripts/rename_project.py`: Migración automática completa
- `scripts/verify_migration.py`: Verificación de migración

### Configuración
- `scripts/setup_complete.py`: Configuración completa
- `scripts/update_env.py`: Actualización de .env

## 📚 Documentación

### Guías
- `MIGRATION_GUIDE.md`: Guía completa de migración
- `CONFIGURATION_GUIDE.md`: Guía de configuración actualizada

### Verificación
- `MIGRATION_SUMMARY.md`: Este resumen

## 🎉 Resultado Final

Después de la migración exitosa, tendrás:

1. **Nuevo proyecto** en Google Cloud: `legislink-ai`
2. **Nueva aplicación** desplegada: `LegisLink AI`
3. **Todos los servicios** configurados con el nuevo nombre
4. **Archivos actualizados** sin referencias al nombre anterior
5. **CI/CD funcionando** con el nuevo proyecto

## 🔍 Verificación Rápida

```bash
# Verificar proyecto actual
gcloud config get-value project

# Verificar servicios
gcloud run services list --region=us-central1

# Verificar archivos
grep -r "legislink-pro" . --exclude-dir=venv --exclude-dir=node_modules

# Ejecutar verificación completa
python scripts/verify_migration.py
```

---

**¡La migración está lista para ejecutarse! 🚀** 