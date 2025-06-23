#!/usr/bin/env python3
"""
Script completo de configuración para LegisLink AI
Configura todos los servicios de Google Cloud necesarios para el proyecto
"""

import os
import subprocess
import json
import time
from pathlib import Path

# Configuración del proyecto
PROJECT_ID = "legislink-ai"
REGION = "us-central1"
ZONE = "us-central1-a"

def run_command(command, description, check=True):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}")
    print(f"   Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Exitoso")
            return result.stdout.strip()
        else:
            print(f"❌ {description} - Falló")
            print(f"   Error: {result.stderr}")
            if check:
                raise Exception(f"Comando falló: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        if check:
            raise
        return None

def check_prerequisites():
    """Verifica los prerrequisitos"""
    print("🔍 Verificando prerrequisitos...")
    
    # Verificar gcloud
    gcloud_version = run_command("gcloud --version", "Verificando gcloud CLI", check=False)
    if not gcloud_version:
        print("❌ gcloud CLI no está instalado")
        print("📝 Instala gcloud desde: https://cloud.google.com/sdk/docs/install")
        return False
    
    # Verificar proyecto
    current_project = run_command("gcloud config get-value project", "Obteniendo proyecto actual", check=False)
    if current_project != PROJECT_ID:
        print(f"⚠️  Proyecto actual: {current_project}")
        print(f"📝 Configurando proyecto: {PROJECT_ID}")
        run_command(f"gcloud config set project {PROJECT_ID}", "Configurando proyecto")
    
    # Verificar facturación
    billing_enabled = run_command(
        "gcloud billing projects describe legislink-ai --format='value(billingEnabled)'",
        "Verificando facturación",
        check=False
    )
    
    if billing_enabled != "True":
        print("❌ La facturación no está habilitada")
        print("📝 Habilita la facturación en: https://console.cloud.google.com/billing")
        return False
    
    print("✅ Prerrequisitos verificados")
    return True

def enable_apis():
    """Habilita las APIs necesarias"""
    print("\n🔌 Habilitando APIs...")
    
    apis = [
        "cloudbuild.googleapis.com",
        "run.googleapis.com",
        "sqladmin.googleapis.com",
        "redis.googleapis.com",
        "aiplatform.googleapis.com",
        "drive.googleapis.com",
        "secretmanager.googleapis.com",
        "artifactregistry.googleapis.com",
        "containerregistry.googleapis.com"
    ]
    
    for api in apis:
        run_command(f"gcloud services enable {api}", f"Habilitando {api}")

def create_service_account():
    """Crea el service account para la aplicación"""
    print("\n👤 Creando service account...")
    
    sa_email = f"legislink-service@{PROJECT_ID}.iam.gserviceaccount.com"

    # Crear service account
    run_command(
        f"gcloud iam service-accounts create legislink-service --display-name='LegisLink Service Account'",
        "Creando service account",
        check=False  # No fallar si ya existe
    )
    
    # Asignar roles
    roles = [
        "roles/cloudsql.client",
        "roles/redis.admin",
        "roles/aiplatform.user",
        # "roles/drive.file", # Removido. El acceso a Drive se configura manualmente compartiendo la carpeta.
        "roles/secretmanager.secretAccessor",
        "roles/storage.objectViewer",
        "roles/logging.logWriter",
        "roles/monitoring.metricWriter"
    ]
    
    for role in roles:
        run_command(
            f"gcloud projects add-iam-policy-binding {PROJECT_ID} --member='serviceAccount:{sa_email}' --role='{role}'",
            f"Asignando rol: {role}",
            check=False # No fallar si el rol ya está asignado
        )

    print("\n" + "="*60)
    print("🔴 ACCIÓN MANUAL REQUERIDA PARA GOOGLE DRIVE 🔴")
    print("="*60)
    print("Para que la aplicación pueda acceder a los documentos, debes compartir")
    print("la carpeta de Google Drive con la siguiente cuenta de servicio:")
    print(f"\n   ==> {sa_email} <==\n")
    print("En Google Drive, haz clic en 'Compartir' en tu carpeta y añade este email.")
    print("Asegúrate de darle permisos de 'Editor'.")
    print("="*60 + "\n")
    
    # Crear y descargar credenciales
    credentials_path = os.path.expanduser("~/legislink-ai-service-key.json")
    run_command(
        f"gcloud iam service-accounts keys create {credentials_path} --iam-account={sa_email}",
        "Creando credenciales del service account"
    )
    
    print(f"✅ Credenciales guardadas en: {credentials_path}")

def setup_cloud_sql():
    """Configura Cloud SQL (MySQL)"""
    print("\n🗄️  Configurando Cloud SQL...")
    
    # Crear instancia de MySQL
    run_command(
        f"gcloud sql instances create legislink-ai-db --database-version=MYSQL_8_0 --tier=db-f1-micro --region={REGION} --root-password=LegisLink2024! --storage-type=SSD --storage-size=10GB",
        "Creando instancia de MySQL",
        check=False
    )
    
    # Crear base de datos
    run_command(
        f"gcloud sql databases create legislink-ai_db --instance=legislink-ai-db",
        "Creando base de datos",
        check=False
    )
    
    # Crear usuario
    run_command(
        f"gcloud sql users create legislink --instance=legislink-ai-db --password=LegisLink2024!",
        "Creando usuario de base de datos",
        check=False
    )
    
    print("✅ Cloud SQL configurado")

def setup_memorystore():
    """Configura MemoryStore (Redis)"""
    print("\n🔴 Configurando MemoryStore...")
    
    run_command(
        f"gcloud redis instances create legislink-ai-redis --size=1 --region={REGION} --redis-version=redis_6_x",
        "Creando instancia de Redis",
        check=False
    )
    
    print("✅ MemoryStore configurado")

def setup_artifact_registry():
    """Configura Artifact Registry"""
    print("\n📦 Configurando Artifact Registry...")
    
    run_command(
        f"gcloud artifacts repositories create legislink-ai-repo --repository-format=docker --location={REGION} --description='Docker repository for LegisLink AI'",
        "Creando repositorio de Docker",
        check=False
    )
    
    # Configurar Docker para usar el repositorio
    run_command(
        f"gcloud auth configure-docker {REGION}-docker.pkg.dev",
        "Configurando Docker para Artifact Registry"
    )
    
    print("✅ Artifact Registry configurado")

def setup_secret_manager():
    """Configura Secret Manager"""
    print("\n🔐 Configurando Secret Manager...")
    
    secrets = [
        "legislink-ai-gemini-key",
        "legislink-ai-db-password",
        "legislink-ai-db-host",
        "legislink-ai-db-name",
        "legislink-ai-db-user",
        "legislink-ai-drive-folder"
    ]
    
    for secret in secrets:
        run_command(
            f"gcloud secrets create {secret} --replication-policy='automatic'",
            f"Creando secret: {secret}",
            check=False
        )
    
    print("✅ Secret Manager configurado")

def setup_vertex_ai():
    """Configura Vertex AI"""
    print("\n🤖 Configurando Vertex AI...")
    
    # Ejecutar script de configuración de Vertex AI
    vertex_script = "scripts/setup_vertex_ai.py"
    if os.path.exists(vertex_script):
        run_command(f"python3 {vertex_script}", "Ejecutando configuración de Vertex AI")
    else:
        print("⚠️  Script de Vertex AI no encontrado")

def setup_gemini():
    """Configura Gemini API"""
    print("\n🔑 Configurando Gemini API...")
    
    # Ejecutar script de configuración de Gemini
    gemini_script = "scripts/setup_gemini.py"
    if os.path.exists(gemini_script):
        run_command(f"python3 {gemini_script}", "Ejecutando configuración de Gemini")
    else:
        print("⚠️  Script de Gemini no encontrado")

def setup_drive():
    """Configura Google Drive"""
    print("\n📁 Configurando Google Drive...")
    
    # Ejecutar script de configuración de Drive
    drive_script = "scripts/setup_drive.py"
    if os.path.exists(drive_script):
        run_command(f"python3 {drive_script}", "Ejecutando configuración de Google Drive")
    else:
        print("⚠️  Script de Google Drive no encontrado")

def update_env_file():
    """Actualiza el archivo .env con todas las credenciales"""
    print("\n📝 Actualizando archivo .env...")
    
    # Ejecutar script de actualización del .env
    update_script = "scripts/update_env.py"
    if os.path.exists(update_script):
        run_command(f"python3 {update_script}", "Actualizando archivo .env")
    else:
        print("⚠️  Script de actualización de .env no encontrado")
        create_env_file()

def create_env_file():
    """Crea el archivo .env con la configuración"""
    
    print("\n📝 Creando archivo .env...")
    
    env_content = """# ========================================
# LEGISLINK PRO - CONFIGURACIÓN DE ENTORNO
# ========================================

# Flask Configuration
FLASK_APP=api.main:app
FLASK_ENV=production
SECRET_KEY=una-clave-secreta-muy-segura-cambiar-en-produccion

# Database Configuration (Cloud SQL)
DB_HOST=legislink-ai-db.legislink-ai.us-central1
DB_PORT=3306
DB_USER=legislink
DB_PASSWORD=LegisLink2024!
DB_NAME=legislink-ai_db

# Redis Configuration (MemoryStore)
REDIS_HOST=10.0.0.3
REDIS_PORT=6379
REDIS_DB=0

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/legislink-ai-service-key.json
GCP_PROJECT_ID=legislink-ai
GCP_REGION=us-central1

# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash

# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=your-google-drive-folder-id

# Vertex AI Configuration
VERTEX_AI_INDEX_ID=projects/legislink-ai/locations/us-central1/indexes/your-index-id
VERTEX_AI_INDEX_ENDPOINT_ID=projects/legislink-ai/locations/us-central1/indexEndpoints/your-endpoint-id

# Constitute Project API
CONSTITUTE_API_KEY=your-constitute-api-key

# Application Configuration
APP_NAME=LegisLink AI
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO

# Security Configuration
CORS_ORIGINS=https://legislink-ai-frontend-xxxxx-uc.a.run.app
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# Performance Configuration
MAX_CONNECTIONS=20
CONNECTION_TIMEOUT=30
REQUEST_TIMEOUT=60

# Monitoring Configuration
ENABLE_METRICS=True
METRICS_PORT=9090
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")
    print("⚠️  IMPORTANTE: Actualiza las siguientes variables en .env:")
    print("   - GEMINI_API_KEY")
    print("   - GOOGLE_DRIVE_FOLDER_ID")
    print("   - VERTEX_AI_INDEX_ID")
    print("   - VERTEX_AI_INDEX_ENDPOINT_ID")
    print("   - CONSTITUTE_API_KEY")

def deploy_services():
    """Despliega los servicios en Cloud Run"""
    print("\n🚀 Desplegando servicios...")
    
    # Desplegar backend
    print("📦 Desplegando backend...")
    run_command(
        f"gcloud run deploy legislink-ai-backend --source . --region={REGION} --platform=managed --allow-unauthenticated --port=5000 --memory=2Gi --cpu=2 --max-instances=10 --service-account=legislink-service@{PROJECT_ID}.iam.gserviceaccount.com",
        "Desplegando backend en Cloud Run"
    )
    
    # Desplegar frontend
    print("📦 Desplegando frontend...")
    run_command(
        f"cd frontend && gcloud run deploy legislink-ai-frontend --source . --region={REGION} --platform=managed --allow-unauthenticated --port=80 --memory=512Mi --cpu=1 --max-instances=5",
        "Desplegando frontend en Cloud Run"
    )

def show_final_instructions():
    """Muestra las instrucciones finales al usuario"""
    
    print("\n\n🎉 ¡Configuración completada!")
    print("============================================================")
    print("🚀 LegisLink AI está casi listo. Pasos finales:")
    
    # Obtener el email del service account
    sa_email = f"legislink-service@{PROJECT_ID}.iam.gserviceaccount.com"
    
    # Obtener el host de la instancia de SQL
    db_host_command = f"gcloud sql instances describe legislink-ai-db --format='value(ipAddresses[0].ipAddress)'"
    db_host = run_command(db_host_command, "Obteniendo IP de Cloud SQL", check=False)
    
    # Obtener el host de la instancia de Redis
    redis_host_command = f"gcloud redis instances describe legislink-ai-redis --region={REGION} --format='value(host)'"
    redis_host = run_command(redis_host_command, "Obteniendo IP de Redis", check=False)

    print(f"""
    1. 📂 **Configura Google Drive:**
       - Ve a Google Drive y crea una nueva carpeta (ej: "LegisLinkDocs").
       - Haz clic derecho en la carpeta > Compartir.
       - Copia y pega el siguiente email del Service Account para compartirlo:
         📧 **{sa_email}**
       - Asegúrate de darle permisos de "Editor".
       - Copia el ID de la carpeta de la URL (la parte después de 'folders/').
       - Guarda este ID en Secret Manager:
         gcloud secrets versions add legislink-ai-drive-folder --data-from-file <(echo -n 'ID_DE_LA_CARPETA')

    2. 🔑 **Configura las credenciales de la base de datos y Gemini:**
       - Guarda la contraseña de la base de datos en Secret Manager:
         gcloud secrets versions add legislink-ai-db-password --data-from-file <(echo -n 'LegisLink2024!')
       - Guarda los datos del host de la base de datos:
         gcloud secrets versions add legislink-ai-db-host --data-from-file <(echo -n '{db_host}')
       - Guarda los demás datos de la base de datos:
         gcloud secrets versions add legislink-ai-db-name --data-from-file <(echo -n 'legislink-ai_db')
         gcloud secrets versions add legislink-ai-db-user --data-from-file <(echo -n 'legislink')
       - Guarda tu API Key de Gemini:
         gcloud secrets versions add legislink-ai-gemini-key --data-from-file <(echo -n 'TU_API_KEY_DE_GEMINI')

    3. ⚙️ **Actualiza tu entorno local:**
       - Ejecuta el siguiente script para poblar tu archivo `.env` con los valores de Secret Manager:
         python3 scripts/update_env.py
         
    4. 🚀 **Despliega la aplicación:**
       - Finalmente, construye y despliega los servicios con Cloud Build:
         gcloud builds submit --config cloudbuild.yaml
    """)

def main():
    """Función principal del script"""
    print("🚀 Iniciando configuración completa de LegisLink AI")
    print("=" * 60)
    
    try:
        # Verificar prerrequisitos
        if not check_prerequisites():
            print("❌ Prerrequisitos no cumplidos. Abortando configuración.")
            return
        
        # Habilitar APIs
        enable_apis()
        
        # Crear service account
        create_service_account()
        
        # Configurar servicios
        setup_cloud_sql()
        setup_memorystore()
        setup_artifact_registry()
        setup_secret_manager()
        
        # Configurar APIs
        setup_vertex_ai()
        setup_gemini()
        setup_drive()
        
        # Actualizar archivo .env
        update_env_file()
        
        # Mostrar instrucciones finales
        show_final_instructions()
        
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        print("📝 Revisa los errores y ejecuta los pasos manualmente si es necesario")

if __name__ == "__main__":
    main() 