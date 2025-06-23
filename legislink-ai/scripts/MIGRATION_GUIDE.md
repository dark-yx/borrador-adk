# 🔄 Guía de Migración: LegisLink Pro → LegisLink AI

## 📋 Resumen

Esta guía te ayudará a migrar el proyecto de `legislink-pro` a `legislink-ai`, actualizando todos los archivos, configuraciones y servicios de Google Cloud.

## 🎯 Migración Automática (Recomendada)

### Paso 1: Ejecutar Script de Migración

```bash
# Navegar al directorio del proyecto
cd legislink-pro

# Ejecutar migración automática
python scripts/rename_project.py
```

Este script automatiza todos los cambios:
- ✅ Actualiza todos los archivos del proyecto
- ✅ Crea nuevo proyecto en Google Cloud
- ✅ Configura nuevos servicios (Cloud SQL, MemoryStore, etc.)
- ✅ Actualiza service accounts y credenciales
- ✅ Renombra el directorio del proyecto

## 🔧 Migración Manual (Paso a Paso)

### Paso 1: Crear Nuevo Proyecto en Google Cloud

```bash
# Crear nuevo proyecto
gcloud projects create legislink-ai --name="LegisLink AI"

# Configurar nuevo proyecto
gcloud config set project legislink-ai

# Habilitar facturación (manual)
# Ve a: https://console.cloud.google.com/billing/projects/legislink-ai
```

### Paso 2: Habilitar APIs en el Nuevo Proyecto

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

### Paso 3: Crear Service Account

```bash
# Crear service account
gcloud iam service-accounts create legislink-ai-service \
  --display-name="LegisLink AI Service Account"

# Asignar roles
gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/redis.admin"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/drive.file"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding legislink-ai \
  --member="serviceAccount:legislink-ai-service@legislink-ai.iam.gserviceaccount.com" \
  --role="roles/monitoring.metricWriter"

# Crear credenciales
gcloud iam service-accounts keys create ~/legislink-ai-service-key.json \
  --iam-account=legislink-ai-service@legislink-ai.iam.gserviceaccount.com
```

### Paso 4: Configurar Servicios

```bash
# Cloud SQL
gcloud sql instances create legislink-ai-db \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=LegisLink2024! \
  --storage-type=SSD \
  --storage-size=10GB

gcloud sql databases create legislink_ai_db --instance=legislink-ai-db
gcloud sql users create legislink-ai --instance=legislink-ai-db --password=LegisLink2024!

# MemoryStore
gcloud redis instances create legislink-ai-redis \
  --size=1 \
  --region=us-central1 \
  --redis-version=redis_6_x

# Artifact Registry
gcloud artifacts repositories create legislink-ai-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for LegisLink AI"

# Secret Manager
gcloud secrets create legislink-ai-gemini-key --replication-policy="automatic"
gcloud secrets create legislink-ai-db-password --replication-policy="automatic"
gcloud secrets create legislink-ai-db-host --replication-policy="automatic"
gcloud secrets create legislink-ai-db-name --replication-policy="automatic"
gcloud secrets create legislink-ai-db-user --replication-policy="automatic"
gcloud secrets create legislink-ai-drive-folder --replication-policy="automatic"
```

### Paso 5: Actualizar Archivos del Proyecto

#### Archivos Principales

1. **env.example**
   ```bash
   # Cambiar todas las referencias de legislink-pro a legislink-ai
   sed -i '' 's/legislink-pro/legislink-ai/g' env.example
   sed -i '' 's/LegisLink Pro/LegisLink AI/g' env.example
   ```

2. **README.md**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' README.md
   sed -i '' 's/LegisLink Pro/LegisLink AI/g' README.md
   ```

3. **CONFIGURATION_GUIDE.md**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' CONFIGURATION_GUIDE.md
   sed -i '' 's/LegisLink Pro/LegisLink AI/g' CONFIGURATION_GUIDE.md
   ```

#### Scripts

4. **scripts/setup_complete.py**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' scripts/setup_complete.py
   ```

5. **scripts/setup_vertex_ai.py**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' scripts/setup_vertex_ai.py
   ```

6. **scripts/update_env.py**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' scripts/update_env.py
   ```

#### Configuración

7. **config/settings.py**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' config/settings.py
   ```

8. **cloudbuild.yaml**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' cloudbuild.yaml
   ```

9. **.github/workflows/deploy.yml**
   ```bash
   sed -i '' 's/legislink-pro/legislink-ai/g' .github/workflows/deploy.yml
   ```

#### Frontend

10. **frontend/package.json**
    ```bash
    sed -i '' 's/legislink-pro/legislink-ai/g' frontend/package.json
    ```

11. **frontend/src/locales/en.json**
    ```bash
    sed -i '' 's/LegisLink Pro/LegisLink AI/g' frontend/src/locales/en.json
    ```

12. **frontend/src/locales/es.json**
    ```bash
    sed -i '' 's/LegisLink Pro/LegisLink AI/g' frontend/src/locales/es.json
    ```

#### Docker

13. **docker-compose.yml** (en el directorio padre)
    ```bash
    cd ..
    sed -i '' 's/legislink-pro/legislink-ai/g' docker-compose.yml
    sed -i '' 's/legislink_net/legislink_ai_net/g' docker-compose.yml
    ```

### Paso 6: Renombrar Directorio

```bash
# Desde el directorio padre
cd ..
mv legislink-pro legislink-ai
cd legislink-ai
```

### Paso 7: Actualizar Configuraciones Específicas

#### Actualizar .env (si existe)

```bash
# Crear nuevo .env con las nuevas configuraciones
cp env.example .env

# Actualizar variables específicas
sed -i '' 's/legislink-db.legislink-pro.us-central1/legislink-ai-db.legislink-ai.us-central1/g' .env
sed -i '' 's/legislink-service@legislink-pro.iam.gserviceaccount.com/legislink-ai-service@legislink-ai.iam.gserviceaccount.com/g' .env
sed -i '' 's/legislink-service-key.json/legislink-ai-service-key.json/g' .env
sed -i '' 's/legislink_db/legislink_ai_db/g' .env
```

#### Actualizar GitHub Secrets

En tu repositorio GitHub, actualiza los secrets:
- `GCP_SA_KEY`: Contenido del nuevo archivo `~/legislink-ai-service-key.json`
- `PROJECT_ID`: `legislink-ai`

## 🔄 Después de la Migración

### Paso 1: Verificar Configuración

```bash
# Verificar proyecto actual
gcloud config get-value project

# Verificar servicios
gcloud run services list --region=us-central1
gcloud sql instances list
gcloud redis instances list --region=us-central1
```

### Paso 2: Ejecutar Configuración Completa

```bash
# Ejecutar configuración completa en el nuevo proyecto
python scripts/setup_complete.py
```

### Paso 3: Actualizar .env

```bash
# Actualizar archivo .env con nuevas credenciales
python scripts/update_env.py
```

### Paso 4: Desplegar

```bash
# Hacer push a GitHub para desplegar automáticamente
git add .
git commit -m "Migrate project to legislink-ai"
git push origin main
```

## 📋 Checklist de Migración

### ✅ Google Cloud
- [ ] Nuevo proyecto `legislink-ai` creado
- [ ] Facturación habilitada
- [ ] APIs habilitadas
- [ ] Service account creado y configurado
- [ ] Cloud SQL configurado
- [ ] MemoryStore configurado
- [ ] Artifact Registry configurado
- [ ] Secret Manager configurado

### ✅ Archivos del Proyecto
- [ ] env.example actualizado
- [ ] README.md actualizado
- [ ] CONFIGURATION_GUIDE.md actualizado
- [ ] Scripts actualizados
- [ ] Configuraciones actualizadas
- [ ] Frontend actualizado
- [ ] Docker configurado

### ✅ Directorio
- [ ] Directorio renombrado de `legislink-pro` a `legislink-ai`

### ✅ Despliegue
- [ ] GitHub secrets actualizados
- [ ] Configuración completa ejecutada
- [ ] .env actualizado
- [ ] Aplicación desplegada y funcionando

## 🔗 URLs Importantes

### Nuevo Proyecto
- **Google Cloud Console**: https://console.cloud.google.com/home/dashboard?project=legislink-ai
- **Facturación**: https://console.cloud.google.com/billing/projects/legislink-ai
- **APIs**: https://console.cloud.google.com/apis/dashboard?project=legislink-ai
- **Cloud Run**: https://console.cloud.google.com/run?project=legislink-ai
- **Cloud SQL**: https://console.cloud.google.com/sql?project=legislink-ai
- **MemoryStore**: https://console.cloud.google.com/memorystore?project=legislink-ai

## 🛠️ Solución de Problemas

### Error: Proyecto no existe
```bash
# Verificar proyectos disponibles
gcloud projects list

# Crear proyecto si no existe
gcloud projects create legislink-ai --name="LegisLink AI"
```

### Error: Facturación no habilitada
```bash
# Verificar facturación
gcloud billing projects describe legislink-ai --format='value(billingEnabled)'

# Habilitar desde la consola web
# https://console.cloud.google.com/billing/projects/legislink-ai
```

### Error: Service account sin permisos
```bash
# Verificar roles
gcloud projects get-iam-policy legislink-ai \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:legislink-ai-service@legislink-ai.iam.gserviceaccount.com"
```

### Error: Archivos no actualizados
```bash
# Ejecutar script de migración
python scripts/rename_project.py
```

## 📚 Recursos Adicionales

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Cloud Run Migration Guide](https://cloud.google.com/run/docs/migrating)
- [ADK Documentation](https://google.github.io/adk-docs/)

---

**¡Listo! Tu proyecto ha sido migrado exitosamente a LegisLink AI. 🎉** 