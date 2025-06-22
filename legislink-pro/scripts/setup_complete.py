#!/usr/bin/env python3
"""
Script completo de configuración para LegisLink Pro
Ejecuta todos los pasos necesarios para configurar el proyecto en Google Cloud
"""

import os
import sys
import subprocess
import json
import time

def run_command(command, description, check=True):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Exitoso")
            if result.stdout:
                print(f"Salida: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ {description} - Falló")
            print(f"Error: {result.stderr}")
            if check:
                return False
            else:
                print("⚠️  Continuando...")
                return True
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        if check:
            return False
        else:
            print("⚠️  Continuando...")
            return True

def setup_project():
    """Configura el proyecto de Google Cloud"""
    
    print("🚀 Iniciando configuración completa de LegisLink Pro")
    print("=" * 60)
    
    # 1. Verificar configuración de gcloud
    if not run_command("gcloud config get-value project", "Verificando proyecto actual"):
        print("❌ Error: No se pudo obtener el proyecto actual")
        return False
    
    # 2. Habilitar APIs necesarias
    apis = [
        "aiplatform.googleapis.com",
        "cloudbuild.googleapis.com", 
        "run.googleapis.com",
        "sqladmin.googleapis.com",
        "redis.googleapis.com",
        "drive.googleapis.com",
        "artifactregistry.googleapis.com",
        "secretmanager.googleapis.com"
    ]
    
    for api in apis:
        if not run_command(f"gcloud services enable {api}", f"Habilitando API: {api}", check=False):
            print(f"⚠️  API {api} no se pudo habilitar (posible problema de facturación)")
    
    # 3. Crear service account si no existe
    if not run_command("gcloud iam service-accounts describe legislink-service@legislink-pro.iam.gserviceaccount.com", "Verificando service account", check=False):
        print("📝 Creando service account...")
        run_command("gcloud iam service-accounts create legislink-service --display-name='LegisLink Service Account' --description='Service account for LegisLink Pro application'", "Creando service account")
    
    # 4. Asignar roles al service account
    roles = [
        "roles/aiplatform.user",
        "roles/cloudsql.client", 
        "roles/storage.objectViewer",
        "roles/secretmanager.secretAccessor",
        "roles/run.admin"
    ]
    
    for role in roles:
        run_command(f"gcloud projects add-iam-policy-binding legislink-pro --member='serviceAccount:legislink-service@legislink-pro.iam.gserviceaccount.com' --role='{role}'", f"Asignando rol: {role}", check=False)
    
    # 5. Crear credenciales del service account
    if not os.path.exists("~/legislink-service-key.json"):
        run_command("gcloud iam service-accounts keys create ~/legislink-service-key.json --iam-account=legislink-service@legislink-pro.iam.gserviceaccount.com", "Creando credenciales del service account")
    
    print("\n✅ Configuración básica del proyecto completada")
    return True

def setup_database():
    """Configura Cloud SQL"""
    
    print("\n🗄️  Configurando Cloud SQL...")
    
    # Verificar si la instancia ya existe
    if run_command("gcloud sql instances describe legislink-db", "Verificando instancia de Cloud SQL", check=False):
        print("✅ Instancia de Cloud SQL ya existe")
        return True
    
    # Crear instancia de Cloud SQL
    if not run_command("gcloud sql instances create legislink-db --database-version=MYSQL_8_0 --tier=db-f1-micro --region=us-central1 --root-password=LegisLink2024! --storage-type=SSD --storage-size=10GB", "Creando instancia de Cloud SQL", check=False):
        print("⚠️  No se pudo crear la instancia de Cloud SQL (verificar facturación)")
        return False
    
    # Crear base de datos
    run_command("gcloud sql databases create legislink_db --instance=legislink-db", "Creando base de datos")
    
    # Crear usuario
    run_command("gcloud sql users create legislink --instance=legislink-db --password=LegisLink2024!", "Creando usuario de base de datos")
    
    print("✅ Configuración de Cloud SQL completada")
    return True

def setup_vertex_ai():
    """Configura Vertex AI"""
    
    print("\n🔍 Configurando Vertex AI...")
    
    # Ejecutar script de configuración de Vertex AI
    if os.path.exists("scripts/setup_vertex_ai.py"):
        run_command("cd scripts && python setup_vertex_ai.py", "Ejecutando configuración de Vertex AI", check=False)
    else:
        print("⚠️  Script de Vertex AI no encontrado")
    
    print("✅ Configuración de Vertex AI completada")
    return True

def setup_secrets():
    """Configura Secret Manager"""
    
    print("\n🔐 Configurando Secret Manager...")
    
    # Ejecutar script de configuración de secrets
    if os.path.exists("scripts/setup_secrets.py"):
        run_command("cd scripts && python setup_secrets.py", "Ejecutando configuración de Secret Manager", check=False)
    else:
        print("⚠️  Script de Secret Manager no encontrado")
    
    print("✅ Configuración de Secret Manager completada")
    return True

def setup_artifact_registry():
    """Configura Artifact Registry"""
    
    print("\n📦 Configurando Artifact Registry...")
    
    # Verificar si el repositorio ya existe
    if run_command("gcloud artifacts repositories describe legislink-repo --location=us-central1", "Verificando repositorio de Artifact Registry", check=False):
        print("✅ Repositorio de Artifact Registry ya existe")
        return True
    
    # Crear repositorio
    if not run_command("gcloud artifacts repositories create legislink-repo --repository-format=docker --location=us-central1 --description='Docker repository for LegisLink Pro'", "Creando repositorio de Artifact Registry", check=False):
        print("⚠️  No se pudo crear el repositorio (verificar facturación)")
        return False
    
    # Configurar Docker
    run_command("gcloud auth configure-docker us-central1-docker.pkg.dev", "Configurando Docker para Artifact Registry")
    
    print("✅ Configuración de Artifact Registry completada")
    return True

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
DB_HOST=legislink-db.legislink-pro.us-central1
DB_PORT=3306
DB_USER=legislink
DB_PASSWORD=LegisLink2024!
DB_NAME=legislink_db

# Redis Configuration (MemoryStore)
REDIS_HOST=10.0.0.3
REDIS_PORT=6379
REDIS_DB=0

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/legislink-service-key.json
GCP_PROJECT_ID=legislink-pro
GCP_REGION=us-central1

# Gemini AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash

# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=your-google-drive-folder-id

# Vertex AI Configuration
VERTEX_AI_INDEX_ID=projects/legislink-pro/locations/us-central1/indexes/your-index-id
VERTEX_AI_INDEX_ENDPOINT_ID=projects/legislink-pro/locations/us-central1/indexEndpoints/your-endpoint-id

# Constitute Project API
CONSTITUTE_API_KEY=your-constitute-api-key

# Application Configuration
APP_NAME=LegisLink Pro
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO

# Security Configuration
CORS_ORIGINS=https://legislink-frontend-xxxxx-uc.a.run.app
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
    
    return True

def main():
    """Función principal"""
    
    print("🚀 Configuración Completa de LegisLink Pro")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("legislink-pro"):
        print("❌ Error: Debes ejecutar este script desde el directorio raíz del proyecto")
        return False
    
    # Cambiar al directorio del proyecto
    os.chdir("legislink-pro")
    
    # Ejecutar configuración paso a paso
    steps = [
        ("Configuración del proyecto", setup_project),
        ("Configuración de Cloud SQL", setup_database),
        ("Configuración de Vertex AI", setup_vertex_ai),
        ("Configuración de Secret Manager", setup_secrets),
        ("Configuración de Artifact Registry", setup_artifact_registry),
        ("Creación del archivo .env", create_env_file)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_func():
            print(f"❌ Error en: {step_name}")
            return False
    
    print("\n" + "="*60)
    print("🎉 ¡Configuración completada exitosamente!")
    print("="*60)
    
    print("\n📋 Próximos pasos:")
    print("1. Actualiza las variables en el archivo .env")
    print("2. Obtén tu API key de Gemini en: https://makersuite.google.com/app/apikey")
    print("3. Configura las credenciales de Google Drive")
    print("4. Configura Vertex AI Search con los scripts en scripts/")
    print("5. Configura los secrets en GitHub para CI/CD")
    print("6. Haz push a GitHub para desplegar automáticamente")
    
    print("\n🔗 URLs importantes:")
    print("- Google Cloud Console: https://console.cloud.google.com")
    print("- Cloud Run: https://console.cloud.google.com/run")
    print("- Cloud SQL: https://console.cloud.google.com/sql")
    print("- Vertex AI: https://console.cloud.google.com/vertex-ai")
    print("- Secret Manager: https://console.cloud.google.com/security/secret-manager")
    
    return True

if __name__ == "__main__":
    main() 