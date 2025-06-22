# 🚀 Guía Completa de Configuración de LegisLink Pro

Esta guía te llevará paso a paso a través de la configuración completa de LegisLink Pro en Google Cloud Platform, incluyendo todas las APIs necesarias y el despliegue CI/CD.

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener:

- ✅ Una cuenta de Google Cloud con facturación habilitada
- ✅ Google Cloud CLI instalado y configurado (`gcloud`)
- ✅ Docker instalado localmente
- ✅ Un repositorio GitHub público
- ✅ Python 3.10+ instalado

## 🔧 Configuración Automática (Recomendado)

### Paso 1: Ejecutar Script de Configuración

```bash
# Desde el directorio raíz del proyecto
cd legislink-pro
python scripts/setup_complete.py
```

Este script automatizará la mayoría de la configuración. Si encuentras errores relacionados con la facturación, sigue la configuración manual.

## 🔧 Configuración Manual (Si es necesario)

### Paso 1: Habilitar Facturación

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Selecciona el proyecto `legislink-pro`
3. Ve a **Billing** → **Link a billing account**
4. Crea una nueva cuenta de facturación o vincula una existente

### Paso 2: Configurar el Proyecto

```bash
# Verificar proyecto actual
gcloud config get-value project

# Si no es el correcto, configurarlo
gcloud config set project legislink-pro
```

### Paso 3: Habilitar APIs

```bash
# APIs necesarias
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable redis.googleapis.com
gcloud services enable drive.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Paso 4: Crear Service Account

```bash
# Crear service account
gcloud iam service-accounts create legislink-service \
  --display-name="LegisLink Service Account" \
  --description="Service account for LegisLink Pro application"

# Asignar roles
gcloud projects add-iam-policy-binding legislink-pro \
  --member="serviceAccount:legislink-service@legislink-pro.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding legislink-pro \
  --member="serviceAccount:legislink-service@legislink-pro.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding legislink-pro \
  --member="serviceAccount:legislink-service@legislink-pro.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

gcloud projects add-iam-policy-binding legislink-pro \
  --member="serviceAccount:legislink-service@legislink-pro.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding legislink-pro \
  --member="serviceAccount:legislink-service@legislink-pro.iam.gserviceaccount.com" \
  --role="roles/run.admin"

# Crear credenciales
gcloud iam service-accounts keys create ~/legislink-service-key.json \
  --iam-account=legislink-service@legislink-pro.iam.gserviceaccount.com
```

### Paso 5: Configurar Cloud SQL

```bash
# Crear instancia de MySQL
gcloud sql instances create legislink-db \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=LegisLink2024! \
  --storage-type=SSD \
  --storage-size=10GB

# Crear base de datos
gcloud sql databases create legislink_db --instance=legislink-db

# Crear usuario
gcloud sql users create legislink \
  --instance=legislink-db \
  --password=LegisLink2024!
```

### Paso 6: Configurar Artifact Registry

```bash
# Crear repositorio de Docker
gcloud artifacts repositories create legislink-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for LegisLink Pro"

# Configurar Docker
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Paso 7: Configurar Secret Manager

```bash
# Crear secrets
gcloud secrets create legislink-gemini-key --replication-policy="automatic"
gcloud secrets create legislink-db-password --replication-policy="automatic"
gcloud secrets create legislink-db-host --replication-policy="automatic"
gcloud secrets create legislink-db-name --replication-policy="automatic"
gcloud secrets create legislink-db-user --replication-policy="automatic"
gcloud secrets create legislink-drive-folder --replication-policy="automatic"
```

## 🔑 Configuración de APIs Externas

### Gemini API

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Haz clic en "Create API Key"
3. Copia la API key generada
4. Agrega la key al archivo `.env`:

```bash
echo "TU_API_KEY_AQUI" | gcloud secrets versions add legislink-gemini-key --data-file=-
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

- `GCP_SA_KEY`: Contenido del archivo `~/legislink-service-key.json`
- `GEMINI_API_KEY`: Tu API key de Gemini
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de Cloud SQL
- `DRIVE_FOLDER_ID`: ID de la carpeta de Google Drive

### Configurar GitHub Actions

El workflow ya está configurado en `.github/workflows/deploy.yml`. Solo necesitas:

1. Hacer push a la rama `main`
2. Verificar que el workflow se ejecute correctamente

## 📝 Configuración del Archivo .env

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
cd legislink-pro
gcloud run deploy legislink-backend \
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
gcloud run deploy legislink-frontend \
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
gcloud run services describe legislink-backend --region=us-central1 --format="value(status.url)"
gcloud run services describe legislink-frontend --region=us-central1 --format="value(status.url)"
```

### Verificar APIs

```bash
# Probar API de Gemini
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'

# Probar Vertex AI
gcloud ai index-endpoints list --region=us-central1
```

## 🛠️ Solución de Problemas

### Error de Facturación

Si encuentras errores relacionados con la facturación:

1. Verifica que la facturación esté habilitada
2. Asegúrate de que la cuenta de facturación esté en buen estado
3. Verifica que no haya límites de cuota

### Error de Permisos

Si encuentras errores de permisos:

```bash
# Verificar roles del service account
gcloud projects get-iam-policy legislink-pro \
  --flatten="bindings[].members" \
  --format="table(bindings.role)" \
  --filter="bindings.members:legislink-service@legislink-pro.iam.gserviceaccount.com"
```

### Error de Conexión a Base de Datos

```bash
# Verificar instancia de Cloud SQL
gcloud sql instances describe legislink-db

# Verificar conexión
gcloud sql connect legislink-db --user=legislink
```

## 📊 Monitoreo

### Cloud Monitoring

1. Ve a [Cloud Monitoring](https://console.cloud.google.com/monitoring)
2. Configura alertas para:
   - Latencia de Cloud Run
   - Uso de CPU y memoria
   - Errores de aplicación
   - Uso de Vertex AI

### Logs

```bash
# Ver logs de Cloud Run
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=legislink-backend" --limit=50

# Ver logs de Vertex AI
gcloud logging read "resource.type=aiplatform_index_endpoint" --limit=50
```

## 🔗 URLs Importantes

- **Google Cloud Console**: https://console.cloud.google.com
- **Cloud Run**: https://console.cloud.google.com/run
- **Cloud SQL**: https://console.cloud.google.com/sql
- **Vertex AI**: https://console.cloud.google.com/vertex-ai
- **Secret Manager**: https://console.cloud.google.com/security/secret-manager
- **Artifact Registry**: https://console.cloud.google.com/artifacts
- **Cloud Build**: https://console.cloud.google.com/cloud-build

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs en Cloud Logging
2. Verifica la configuración en Google Cloud Console
3. Consulta la documentación oficial de Google Cloud
4. Revisa los issues en el repositorio de GitHub

---

¡Felicitaciones! 🎉 Tu aplicación LegisLink Pro está ahora completamente configurada y desplegada en Google Cloud Platform.
