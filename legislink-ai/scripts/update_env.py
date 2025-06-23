#!/usr/bin/env python3
"""
Script para actualizar automáticamente el archivo .env con todas las credenciales generadas
durante el proceso de configuración de LegisLink AI
"""

import os
import json
import subprocess
import re
from pathlib import Path

class EnvUpdater:
    def __init__(self):
        self.project_id = "legislink-ai"
        self.region = "us-central1"
        self.env_file = ".env"
        self.env_vars = {}
        
    def run_command(self, command, description):
        """Ejecuta un comando y maneja errores"""
        print(f"🔄 {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description} - Exitoso")
                return result.stdout.strip()
            else:
                print(f"❌ {description} - Falló: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            return None
    
    def get_cloud_sql_connection_info(self):
        """Obtiene información de conexión de Cloud SQL"""
        print("\n🗄️  Obteniendo información de Cloud SQL...")
        
        # Obtener connection name
        connection_name = self.run_command(
            "gcloud sql instances describe legislink-ai-db --format='value(connectionName)'",
            "Obteniendo connection name de Cloud SQL"
        )
        
        if connection_name:
            # Construir host de conexión
            db_host = f"{connection_name}"
            self.env_vars.update({
                'DB_HOST': db_host,
                'DB_PORT': '3306',
                'DB_USER': 'legislink',
                'DB_PASSWORD': 'LegisLink2024!',
                'DB_NAME': 'legislink-ai_db'
            })
            print(f"✅ DB_HOST configurado: {db_host}")
        else:
            print("⚠️  No se pudo obtener información de Cloud SQL")
    
    def get_service_account_credentials_path(self):
        """Obtiene la ruta de las credenciales del service account"""
        print("\n🔑 Obteniendo credenciales del service account...")
        
        # Verificar si existe el archivo de credenciales
        credentials_path = os.path.expanduser("~/legislink-ai-service-key.json")
        if os.path.exists(credentials_path):
            # Para Cloud Run, usar ruta dentro del contenedor
            container_path = "/app/credentials/legislink-ai-service-key.json"
            self.env_vars.update({
                'GOOGLE_APPLICATION_CREDENTIALS': container_path
            })
            print(f"✅ Credenciales configuradas: {container_path}")
        else:
            print("⚠️  Archivo de credenciales no encontrado")
    
    def get_vertex_ai_config(self):
        """Obtiene configuración de Vertex AI"""
        print("\n🔍 Obteniendo configuración de Vertex AI...")
        
        # Verificar si existe archivo de configuración
        config_file = "vertex_ai_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                self.env_vars.update({
                    'VERTEX_AI_INDEX_ID': config.get('index_id', ''),
                    'VERTEX_AI_INDEX_ENDPOINT_ID': config.get('endpoint_id', '')
                })
                print("✅ Configuración de Vertex AI cargada")
            except Exception as e:
                print(f"❌ Error cargando configuración de Vertex AI: {e}")
        else:
            print("⚠️  Archivo de configuración de Vertex AI no encontrado")
    
    def get_drive_config(self):
        """Obtiene configuración de Google Drive"""
        print("\n📁 Obteniendo configuración de Google Drive...")
        
        # Verificar si existe archivo de configuración
        config_file = "drive_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                self.env_vars.update({
                    'GOOGLE_DRIVE_FOLDER_ID': config.get('drive_folder_id', '')
                })
                print("✅ Configuración de Google Drive cargada")
            except Exception as e:
                print(f"❌ Error cargando configuración de Google Drive: {e}")
        else:
            print("⚠️  Archivo de configuración de Google Drive no encontrado")
    
    def get_cloud_run_urls(self):
        """Obtiene URLs de los servicios de Cloud Run"""
        print("\n🌐 Obteniendo URLs de Cloud Run...")
        
        # Obtener URL del backend
        backend_url = self.run_command(
            "gcloud run services describe legislink-ai-backend --region=us-central1 --format='value(status.url)'",
            "Obteniendo URL del backend"
        )
        
        # Obtener URL del frontend
        frontend_url = self.run_command(
            "gcloud run services describe legislink-ai-frontend --region=us-central1 --format='value(status.url)'",
            "Obteniendo URL del frontend"
        )
        
        if backend_url:
            self.env_vars.update({
                'BACKEND_URL': backend_url
            })
            print(f"✅ Backend URL: {backend_url}")
        
        if frontend_url:
            self.env_vars.update({
                'FRONTEND_URL': frontend_url,
                'CORS_ORIGINS': frontend_url
            })
            print(f"✅ Frontend URL: {frontend_url}")
    
    def get_memorystore_info(self):
        """Obtiene información de MemoryStore (Redis)"""
        print("\n🔴 Obteniendo información de MemoryStore...")
        
        # Obtener IP de MemoryStore
        redis_host = self.run_command(
            "gcloud redis instances describe legislink-ai-redis --region=us-central1 --format='value(host)'",
            "Obteniendo host de MemoryStore"
        )
        
        if redis_host:
            self.env_vars.update({
                'REDIS_HOST': redis_host,
                'REDIS_PORT': '6379',
                'REDIS_DB': '0'
            })
            print(f"✅ Redis configurado: {redis_host}")
        else:
            print("⚠️  No se pudo obtener información de MemoryStore")
    
    def generate_secret_key(self):
        """Genera una clave secreta segura"""
        import secrets
        secret_key = secrets.token_urlsafe(32)
        self.env_vars.update({
            'SECRET_KEY': secret_key
        })
        print("✅ Clave secreta generada")
    
    def prompt_for_gemini_key(self):
        """Solicita la API key de Gemini al usuario"""
        print("\n🔑 Configuración de Gemini API...")
        print("📝 Para obtener tu API key de Gemini:")
        print("1. Ve a: https://makersuite.google.com/app/apikey")
        print("2. Haz clic en 'Create API Key'")
        print("3. Copia la API key generada")
        
        gemini_key = input("\n🔑 Ingresa tu API key de Gemini (o presiona Enter para saltar): ").strip()
        
        if gemini_key:
            self.env_vars.update({
                'GEMINI_API_KEY': gemini_key
            })
            print("✅ API key de Gemini configurada")
        else:
            print("⚠️  API key de Gemini no configurada")
    
    def prompt_for_constitute_key(self):
        """Solicita la API key de Constitute Project al usuario"""
        print("\n�� Configuración de Constitute Project API...")
        print("📝 Para obtener tu API key de Constitute Project:")
        print("1. Ve a: https://www.constituteproject.org/")
        print("2. Regístrate para obtener acceso a la API")
        
        constitute_key = input("\n🔑 Ingresa tu API key de Constitute Project (o presiona Enter para saltar): ").strip()
        
        if constitute_key:
            self.env_vars.update({
                'CONSTITUTE_API_KEY': constitute_key
            })
            print("✅ API key de Constitute Project configurada")
        else:
            print("⚠️  API key de Constitute Project no configurada")
    
    def create_env_content(self):
        """Crea el contenido del archivo .env"""
        env_content = f"""# ========================================
# LEGISLINK PRO - CONFIGURACIÓN DE ENTORNO
# ========================================
# Archivo generado automáticamente por update_env.py
# Fecha de generación: {self.get_current_timestamp()}

# Flask Configuration
FLASK_APP=api.main:app
FLASK_ENV=production
SECRET_KEY={self.env_vars.get('SECRET_KEY', 'una-clave-secreta-muy-segura-cambiar-en-produccion')}

# Database Configuration (Cloud SQL)
DB_HOST={self.env_vars.get('DB_HOST', 'legislink-ai-db.legislink-ai.us-central1')}
DB_PORT={self.env_vars.get('DB_PORT', '3306')}
DB_USER={self.env_vars.get('DB_USER', 'legislink')}
DB_PASSWORD={self.env_vars.get('DB_PASSWORD', 'LegisLink2024!')}
DB_NAME={self.env_vars.get('DB_NAME', 'legislink-ai_db')}

# Redis Configuration (MemoryStore)
REDIS_HOST={self.env_vars.get('REDIS_HOST', '10.0.0.3')}
REDIS_PORT={self.env_vars.get('REDIS_PORT', '6379')}
REDIS_DB={self.env_vars.get('REDIS_DB', '0')}

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS={self.env_vars.get('GOOGLE_APPLICATION_CREDENTIALS', '/app/credentials/legislink-ai-service-key.json')}
GCP_PROJECT_ID={self.project_id}
GCP_REGION={self.region}

# Gemini AI Configuration
GEMINI_API_KEY={self.env_vars.get('GEMINI_API_KEY', 'your-gemini-api-key-here')}
GEMINI_MODEL=gemini-2.0-flash

# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID={self.env_vars.get('GOOGLE_DRIVE_FOLDER_ID', 'your-google-drive-folder-id')}

# Vertex AI Configuration
VERTEX_AI_INDEX_ID={self.env_vars.get('VERTEX_AI_INDEX_ID', 'projects/legislink-ai/locations/us-central1/indexes/your-index-id')}
VERTEX_AI_INDEX_ENDPOINT_ID={self.env_vars.get('VERTEX_AI_INDEX_ENDPOINT_ID', 'projects/legislink-ai/locations/us-central1/indexEndpoints/your-endpoint-id')}

# Constitute Project API
CONSTITUTE_API_KEY={self.env_vars.get('CONSTITUTE_API_KEY', 'your-constitute-api-key')}

# Application Configuration
APP_NAME=LegisLink AI
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO

# Security Configuration
CORS_ORIGINS={self.env_vars.get('CORS_ORIGINS', 'https://legislink-ai-frontend-xxxxx-uc.a.run.app')}
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# Performance Configuration
MAX_CONNECTIONS=20
CONNECTION_TIMEOUT=30
REQUEST_TIMEOUT=60

# Monitoring Configuration
ENABLE_METRICS=True
METRICS_PORT=9090

# Service URLs (generadas automáticamente)
BACKEND_URL={self.env_vars.get('BACKEND_URL', 'https://legislink-ai-backend-us-central1-legislink-ai.a.run.app')}
FRONTEND_URL={self.env_vars.get('FRONTEND_URL', 'https://legislink-ai-frontend-us-central1-legislink-ai.a.run.app')}
"""
        return env_content
    
    def get_current_timestamp(self):
        """Obtiene la fecha y hora actual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def save_env_file(self):
        """Guarda el archivo .env"""
        print(f"\n📝 Guardando archivo {self.env_file}...")
        
        env_content = self.create_env_content()
        
        try:
            with open(self.env_file, 'w') as f:
                f.write(env_content)
            
            print(f"✅ Archivo {self.env_file} guardado exitosamente")
            print(f"📊 Variables configuradas: {len(self.env_vars)}")
            
            # Mostrar resumen de variables configuradas
            print("\n📋 Resumen de configuración:")
            for key, value in self.env_vars.items():
                if 'KEY' in key or 'PASSWORD' in key:
                    print(f"  {key}: {'*' * len(str(value))}")
                else:
                    print(f"  {key}: {value}")
                    
        except Exception as e:
            print(f"❌ Error guardando archivo {self.env_file}: {e}")
    
    def update_secrets_in_gcp(self):
        """Actualiza los secrets en Google Cloud Secret Manager"""
        print("\n🔐 Actualizando secrets en Google Cloud...")
        
        # Actualizar secrets con los valores del .env
        secrets_to_update = {
            'legislink-ai-gemini-key': self.env_vars.get('GEMINI_API_KEY'),
            'legislink-ai-db-password': self.env_vars.get('DB_PASSWORD'),
            'legislink-ai-db-host': self.env_vars.get('DB_HOST'),
            'legislink-ai-db-name': self.env_vars.get('DB_NAME'),
            'legislink-ai-db-user': self.env_vars.get('DB_USER'),
            'legislink-ai-drive-folder': self.env_vars.get('GOOGLE_DRIVE_FOLDER_ID')
        }
        
        for secret_name, secret_value in secrets_to_update.items():
            if secret_value and secret_value not in ['your-gemini-api-key-here', 'your-google-drive-folder-id']:
                self.run_command(
                    f'echo -n "{secret_value}" | gcloud secrets versions add {secret_name} --data-file=-',
                    f"Actualizando secret: {secret_name}"
                )
    
    def run(self):
        """Ejecuta el proceso completo de actualización"""
        print("🚀 Iniciando actualización automática del archivo .env")
        print("=" * 60)
        
        # Obtener información de Google Cloud
        self.get_cloud_sql_connection_info()
        self.get_service_account_credentials_path()
        self.get_vertex_ai_config()
        self.get_drive_config()
        self.get_cloud_run_urls()
        self.get_memorystore_info()
        
        # Generar clave secreta
        self.generate_secret_key()
        
        # Solicitar APIs externas
        self.prompt_for_gemini_key()
        self.prompt_for_constitute_key()
        
        # Guardar archivo .env
        self.save_env_file()
        
        # Actualizar secrets en GCP
        self.update_secrets_in_gcp()
        
        print("\n" + "=" * 60)
        print("🎉 ¡Actualización del archivo .env completada!")
        print("=" * 60)
        
        print("\n📋 Próximos pasos:")
        print("1. Verifica que el archivo .env contenga todas las variables necesarias")
        print("2. Si faltan algunas variables, ejecuta los scripts de configuración correspondientes")
        print("3. Haz push a GitHub para desplegar automáticamente")
        print("4. Verifica que la aplicación funcione correctamente en Cloud Run")

def main():
    """Función principal"""
    updater = EnvUpdater()
    updater.run()

if __name__ == "__main__":
    main()
