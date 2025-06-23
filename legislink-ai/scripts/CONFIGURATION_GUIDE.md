# 🚀 Guía de Configuración Completa - LegisLink AI

## 📋 Resumen

Esta guía te ayudará a configurar completamente LegisLink AI en Google Cloud Platform, incluyendo todos los servicios necesarios, APIs y credenciales.

## 🎯 Configuración Automática (Recomendada)

### Paso 1: Ejecutar Configuración Completa

```bash
# Navegar al directorio del proyecto
cd legislink-ai

# Ejecutar configuración automática completa
python scripts/setup_complete.py
```

Este script automatiza todos los pasos de configuración:
- ✅ Verifica prerrequisitos
- ✅ Habilita APIs necesarias
- ✅ Crea service accounts
- ✅ Configura Cloud SQL, MemoryStore, Artifact Registry
- ✅ Configura Secret Manager
- ✅ Ejecuta scripts de Vertex AI, Gemini y Google Drive
- ✅ **Actualiza automáticamente el archivo .env con todas las credenciales**

### Paso 2: Actualización Automática del .env

El script `setup_complete.py` incluye automáticamente la actualización del archivo `.env`. Si necesitas actualizarlo manualmente:

```bash
# Actualizar archivo .env con todas las credenciales generadas
python scripts/update_env.py
```

Este script:
- 🔍 Obtiene información de Cloud SQL, MemoryStore, Cloud Run
- 🔑 Detecta credenciales del service account
- 📁 Carga configuraciones de Vertex AI y Google Drive
- 🔐 Genera clave secreta segura
- 📝 Solicita APIs externas (Gemini, Constitute Project)
- 💾 Guarda todo en el archivo `.env`
- 🔐 Actualiza secrets en Google Cloud Secret Manager

## 🔧 Configuración Manual (Paso a Paso)

### Prerrequisitos

1. **Google Cloud CLI instalado**
   ```bash
   # Instalar gcloud CLI
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   ```

2. **Proyecto de Google Cloud creado**
   ```bash
   # Crear proyecto
   gcloud projects create legislink-ai --name="LegisLink AI"
   
   # Configurar proyecto
   gcloud config set project legislink-ai
   ```

3. **Facturación habilitada**
   - Ve a [Google Cloud Console - Billing](https://console.cloud.google.com/billing)
   - Vincula una cuenta de facturación al proyecto

### Paso 1: Habilitar APIs

```bash
# APIs necesarias
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable drive.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Paso 2: Crear Service Account

```bash
# Crear service account
gcloud iam service-accounts create legislink-service \
  --display-name="LegisLink Service Account"

# Asignar roles
gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/redis.admin"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/drive.file"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/monitoring.metricWriter"

# Crear y descargar credenciales
gcloud iam service-accounts keys create ~/legislink-ai-service-key.json \
  --iam-account=legislink-service@legislink-ai.iam.gserviceaccount.com
```

### Paso 3: Configurar Cloud SQL

```bash
# Crear instancia de MySQL
gcloud sql instances create legislink-ai-db \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=LegisLink2024! \
  --storage-type=SSD \
  --storage-size=10GB

# Crear base de datos
gcloud sql databases create legislink-ai_db --instance=legislink-ai-db

# Crear usuario
gcloud sql users create legislink \
  --instance=legislink-ai-db \
  --password=LegisLink2024!
```

### Paso 4: Configurar MemoryStore

```bash
# Crear instancia de Redis
gcloud redis instances create legislink-ai-redis \
  --size=1 \
  --region=us-central1 \
  --redis-version=redis_6_x
```

### Paso 5: Configurar Artifact Registry

```bash
# Crear repositorio de Docker
gcloud artifacts repositories create legislink-ai-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for LegisLink AI"

# Configurar Docker para usar el repositorio
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Paso 6: Configurar Secret Manager

```bash
# Crear secrets
gcloud secrets create legislink-ai-gemini-key --replication-policy="automatic"
gcloud secrets create legislink-ai-db-password --replication-policy="automatic"
gcloud secrets create legislink-ai-db-host --replication-policy="automatic"
gcloud secrets create legislink-ai-db-name --replication-policy="automatic"
gcloud secrets create legislink-ai-db-user --replication-policy="automatic"
gcloud secrets create legislink-ai-drive-folder --replication-policy="automatic"
```

## 🔑 Configuración de APIs Externas

### Gemini API

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Haz clic en "Create API Key"
3. Copia la API key generada
4. Agrega la key al archivo `.env`:

```bash
echo "TU_API_KEY_AQUI" | gcloud secrets versions add legislink-ai-gemini-key --data-file=-
```

### Google Drive API

1. Ve a [Google Cloud Console - APIs & Services](https://console.cloud.google.com/apis/credentials)
2. Crea credenciales OAuth 2.0
3. Descarga el archivo JSON
4. Ejecuta el script de configuración:

```bash
cd scripts
python setup_drive.py
```

### Vertex AI Search

1. Ejecuta el script de configuración:

```bash
cd scripts
python setup_vertex_ai.py
```

2. Actualiza las variables en `.env` con los IDs generados

## 🔄 Configuración de CI/CD

### GitHub Secrets

En tu repositorio GitHub, ve a **Settings** → **Secrets and variables** → **Actions** y agrega:

- `GCP_SA_KEY`: Contenido del archivo `~/legislink-ai-service-key.json`
- `GEMINI_API_KEY`: Tu API key de Gemini
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de Cloud SQL
- `DRIVE_FOLDER_ID`: ID de la carpeta de Google Drive

### Configurar GitHub Actions

El workflow ya está configurado en `.github/workflows/deploy.yml`. Solo necesitas:

1. Hacer push a la rama `main`
2. Verificar que el workflow se ejecute correctamente

## 📝 Configuración del Archivo .env

### Actualización Automática (Recomendada)

```bash
# Actualizar automáticamente con todas las credenciales
python scripts/update_env.py
```

### Configuración Manual

Copia `env.example` a `.env` y actualiza las siguientes variables:

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar variables importantes
nano .env
```

Variables que debes actualizar:

- `GEMINI_API_KEY`: Tu API key de Gemini
- `GOOGLE_DRIVE_FOLDER_ID`: ID de la carpeta de Drive
- `VERTEX_AI_INDEX_ID`: ID del índice de Vertex AI
- `VERTEX_AI_INDEX_ENDPOINT_ID`: ID del endpoint de Vertex AI
- `CONSTITUTE_API_KEY`: API key de Constitute Project (opcional)

## 🚀 Despliegue

### Despliegue Automático (Recomendado)

```bash
# Hacer push a GitHub
git add .
git commit -m "Initial deployment configuration"
git push origin main
```

El workflow de GitHub Actions se ejecutará automáticamente y desplegará la aplicación.

### Despliegue Manual

```bash
# Construir y desplegar backend
cd legislink-ai
gcloud run deploy legislink-ai-backend \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=5000 \
  --memory=2Gi \
  --cpu=2 \
  --max-instances=10

# Construir y desplegar frontend
cd frontend
gcloud run deploy legislink-ai-frontend \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=80 \
  --memory=512Mi \
  --cpu=1 \
  --max-instances=5
```

## 🔍 Verificación

### Verificar Despliegue

```bash
# Listar servicios de Cloud Run
gcloud run services list --region=us-central1

# Obtener URLs de los servicios
gcloud run services describe legislink-ai-backend --region=us-central1 --format="value(status.url)"
gcloud run services describe legislink-ai-frontend --region=us-central1 --format="value(status.url)"
```

### Verificar APIs

```bash
# Probar API de Gemini
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'

# Probar Vertex AI
curl -X POST "https://us-central1-aiplatform.googleapis.com/v1/projects/legislink-ai/locations/us-central1/indexEndpoints/YOUR_ENDPOINT_ID:findNeighbors" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"deployed_index_id":"YOUR_DEPLOYED_INDEX_ID","queries":[{"datapoint":{"datapoint_id":"test","feature_vector":[0.1,0.2,0.3]}}],"num_neighbors":5}'
```

## 🛠️ Scripts Disponibles

### Scripts de Configuración

- `scripts/setup_complete.py`: Configuración completa automática
- `scripts/update_env.py`: Actualización automática del archivo .env
- `scripts/setup_vertex_ai.py`: Configuración de Vertex AI
- `scripts/setup_gemini.py`: Configuración de Gemini API
- `scripts/setup_drive.py`: Configuración de Google Drive
- `scripts/setup_secrets.py`: Gestión de Secret Manager

### Uso de los Scripts

```bash
# Configuración completa
python scripts/setup_complete.py

# Actualizar .env con credenciales
python scripts/update_env.py

# Configurar servicios específicos
python scripts/setup_vertex_ai.py
python scripts/setup_gemini.py
python scripts/setup_drive.py
```

## 🔧 Solución de Problemas

### Error: Facturación no habilitada

```bash
# Verificar facturación
gcloud billing projects describe legislink-ai --format='value(billingEnabled)'

# Si es False, habilitar facturación desde la consola web
```

### Error: APIs no habilitadas

```bash
# Habilitar todas las APIs necesarias
python scripts/setup_complete.py
```

### Error: Service account sin permisos

```bash
# Verificar roles del service account
gcloud projects get-iam-policy legislink-ai \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:legislink-service@legislink-ai.iam.gserviceaccount.com"
```

### Error: Archivo .env no actualizado

```bash
# Actualizar manualmente
python scripts/update_env.py
```

## 📊 Monitoreo y Logs

### Ver Logs de Cloud Run

```bash
# Logs del backend
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=legislink-ai-backend" --limit=50

# Logs del frontend
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=legislink-ai-frontend" --limit=50
```

### Ver Métricas

```bash
# Abrir Cloud Monitoring
gcloud monitoring dashboards list
```

## 🎯 Próximos Pasos

1. ✅ Ejecutar configuración completa: `python scripts/setup_complete.py`
2. ✅ Verificar archivo .env: `python scripts/update_env.py`
3. ✅ Hacer push a GitHub para despliegue automático
4. ✅ Verificar funcionamiento en Cloud Run
5. ✅ Configurar monitoreo y alertas
6. ✅ Documentar APIs y endpoints

## 📚 Recursos Adicionales

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [ADK Documentation](https://google.github.io/adk-docs/)

---

**¡Listo! Tu aplicación LegisLink AI está configurada y lista para usar. 🎉**
