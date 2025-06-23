#!/usr/bin/env python3
"""
Script de ayuda para LegisLink AI
Muestra todas las opciones disponibles para configuración y migración
"""

import os
import sys

def show_help():
    """Muestra la ayuda principal"""
    print("🚀 LegisLink AI - Scripts de Ayuda")
    print("=" * 50)
    
    print("\n📋 Scripts Disponibles:")
    print("=" * 30)
    
    scripts = [
        {
            "name": "setup_complete.py",
            "description": "Configuración completa automática del proyecto",
            "usage": "python scripts/setup_complete.py"
        },
        {
            "name": "update_env.py",
            "description": "Actualiza automáticamente el archivo .env con credenciales",
            "usage": "python scripts/update_env.py"
        },
        {
            "name": "rename_project.py",
            "description": "Migra el proyecto de legislink-pro a legislink-ai",
            "usage": "python scripts/rename_project.py"
        },
        {
            "name": "verify_migration.py",
            "description": "Verifica que la migración se completó correctamente",
            "usage": "python scripts/verify_migration.py"
        },
        {
            "name": "setup_vertex_ai.py",
            "description": "Configura Vertex AI Search",
            "usage": "python scripts/setup_vertex_ai.py"
        },
        {
            "name": "setup_gemini.py",
            "description": "Configura Gemini API",
            "usage": "python scripts/setup_gemini.py"
        },
        {
            "name": "setup_drive.py",
            "description": "Configura Google Drive API",
            "usage": "python scripts/setup_drive.py"
        },
        {
            "name": "setup_secrets.py",
            "description": "Gestiona Secret Manager",
            "usage": "python scripts/setup_secrets.py"
        }
    ]
    
    for script in scripts:
        print(f"\n🔧 {script['name']}")
        print(f"   📝 {script['description']}")
        print(f"   💻 {script['usage']}")
    
    print("\n📚 Documentación:")
    print("=" * 20)
    docs = [
        ("README.md", "Documentación principal del proyecto"),
        ("CONFIGURATION_GUIDE.md", "Guía completa de configuración"),
        ("MIGRATION_GUIDE.md", "Guía de migración a legislink-ai"),
        ("MIGRATION_SUMMARY.md", "Resumen de cambios de migración")
    ]
    
    for doc, description in docs:
        if os.path.exists(doc):
            print(f"   ✅ {doc} - {description}")
        else:
            print(f"   ❌ {doc} - {description} (no encontrado)")
    
    print("\n🚀 Flujos de Trabajo Comunes:")
    print("=" * 30)
    
    workflows = [
        {
            "name": "Configuración Inicial",
            "steps": [
                "python scripts/setup_complete.py",
                "python scripts/update_env.py",
                "git add . && git commit -m 'Initial setup'",
                "git push origin main"
            ]
        },
        {
            "name": "Migración a LegisLink AI",
            "steps": [
                "python scripts/rename_project.py",
                "python scripts/verify_migration.py",
                "python scripts/setup_complete.py",
                "python scripts/update_env.py",
                "git add . && git commit -m 'Migrate to legislink-ai'",
                "git push origin main"
            ]
        },
        {
            "name": "Actualización de Credenciales",
            "steps": [
                "python scripts/update_env.py",
                "git add .env && git commit -m 'Update credentials'",
                "git push origin main"
            ]
        }
    ]
    
    for i, workflow in enumerate(workflows, 1):
        print(f"\n{i}. {workflow['name']}:")
        for j, step in enumerate(workflow['steps'], 1):
            print(f"   {j}. {step}")
    
    print("\n🔍 Comandos de Verificación:")
    print("=" * 30)
    verification_commands = [
        ("gcloud config get-value project", "Verificar proyecto actual"),
        ("gcloud run services list --region=us-central1", "Listar servicios de Cloud Run"),
        ("gcloud sql instances list", "Listar instancias de Cloud SQL"),
        ("gcloud redis instances list --region=us-central1", "Listar instancias de Redis"),
        ("python scripts/verify_migration.py", "Verificación completa de migración")
    ]
    
    for command, description in verification_commands:
        print(f"   💻 {command}")
        print(f"      📝 {description}")
    
    print("\n📞 Soporte:")
    print("=" * 15)
    print("   📚 Documentación: CONFIGURATION_GUIDE.md")
    print("   🔄 Migración: MIGRATION_GUIDE.md")
    print("   🔍 Verificación: python scripts/verify_migration.py")
    print("   🚀 Despliegue: git push origin main")

def show_script_help(script_name):
    """Muestra ayuda específica para un script"""
    script_help = {
        "setup_complete.py": """
🔧 setup_complete.py - Configuración Completa Automática

📝 Descripción:
   Configura automáticamente todos los servicios de Google Cloud necesarios
   para LegisLink AI, incluyendo APIs, service accounts, Cloud SQL, MemoryStore,
   Artifact Registry, Secret Manager y más.

🚀 Uso:
   python scripts/setup_complete.py

✅ Lo que hace:
   - Verifica prerrequisitos (gcloud, facturación)
   - Habilita APIs necesarias
   - Crea service account con roles apropiados
   - Configura Cloud SQL (MySQL)
   - Configura MemoryStore (Redis)
   - Configura Artifact Registry
   - Configura Secret Manager
   - Ejecuta scripts de Vertex AI, Gemini y Drive
   - Actualiza archivo .env
   - Muestra instrucciones finales

⚠️  Requisitos:
   - gcloud CLI instalado y autenticado
   - Facturación habilitada en Google Cloud
   - Proyecto creado en Google Cloud
""",
        
        "update_env.py": """
🔧 update_env.py - Actualización Automática del .env

📝 Descripción:
   Actualiza automáticamente el archivo .env con todas las credenciales
   generadas durante el proceso de configuración.

🚀 Uso:
   python scripts/update_env.py

✅ Lo que hace:
   - Obtiene información de Cloud SQL
   - Detecta credenciales del service account
   - Carga configuraciones de Vertex AI y Google Drive
   - Genera clave secreta segura
   - Solicita APIs externas (Gemini, Constitute Project)
   - Guarda todo en el archivo .env
   - Actualiza secrets en Google Cloud Secret Manager

📋 Variables que actualiza:
   - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
   - REDIS_HOST, REDIS_PORT, REDIS_DB
   - GOOGLE_APPLICATION_CREDENTIALS
   - GEMINI_API_KEY
   - GOOGLE_DRIVE_FOLDER_ID
   - VERTEX_AI_INDEX_ID, VERTEX_AI_INDEX_ENDPOINT_ID
   - CONSTITUTE_API_KEY
   - SECRET_KEY
   - BACKEND_URL, FRONTEND_URL
""",
        
        "rename_project.py": """
🔧 rename_project.py - Migración a LegisLink AI

📝 Descripción:
   Migra el proyecto de legislink-pro a legislink-ai, actualizando
   todos los archivos, configuraciones y servicios de Google Cloud.

🚀 Uso:
   python scripts/rename_project.py

✅ Lo que hace:
   - Actualiza todos los archivos del proyecto
   - Crea nuevo proyecto en Google Cloud
   - Configura nuevos servicios (Cloud SQL, MemoryStore, etc.)
   - Actualiza service accounts y credenciales
   - Renombra el directorio del proyecto

🔄 Cambios principales:
   - Proyecto: legislink-pro → legislink-ai
   - Nombre: LegisLink Pro → LegisLink AI
   - Service Account: legislink-service → legislink-ai-service
   - Base de datos: legislink_db → legislink_ai_db
   - Redis: legislink-redis → legislink-ai-redis
   - Repositorio Docker: legislink-repo → legislink-ai-repo

⚠️  Importante:
   - Habilita la facturación para el nuevo proyecto
   - Actualiza GitHub secrets después de la migración
""",
        
        "verify_migration.py": """
🔧 verify_migration.py - Verificación de Migración

📝 Descripción:
   Verifica que la migración de legislink-pro a legislink-ai
   se ha completado correctamente.

🚀 Uso:
   python scripts/verify_migration.py

✅ Lo que verifica:
   - Proyecto de Google Cloud configurado correctamente
   - Service account creado y configurado
   - Cloud SQL configurado
   - MemoryStore configurado
   - Artifact Registry configurado
   - Secret Manager configurado
   - APIs habilitadas
   - Archivos del proyecto actualizados
   - Estructura de directorios correcta

📊 Genera un reporte con:
   - Total de verificaciones
   - Verificaciones exitosas y fallidas
   - Porcentaje de éxito
   - Detalles de cada verificación
   - Próximos pasos recomendados
""",
        
        "setup_vertex_ai.py": """
🔧 setup_vertex_ai.py - Configuración de Vertex AI

📝 Descripción:
   Configura Vertex AI Search para búsqueda semántica en documentos legales.

🚀 Uso:
   python scripts/setup_vertex_ai.py

✅ Lo que hace:
   - Inicializa Vertex AI
   - Crea índice de búsqueda vectorial
   - Crea endpoint para el índice
   - Despliega el índice al endpoint
   - Guarda configuración en archivo JSON

📋 Configuración:
   - Proyecto: legislink-ai
   - Región: us-central1
   - Índice: legislink-ai-legal-docs
   - Endpoint: legislink-ai-search-endpoint
   - Dimensiones: 768 (modelo de embedding)
""",
        
        "setup_gemini.py": """
🔧 setup_gemini.py - Configuración de Gemini API

📝 Descripción:
   Configura la API de Gemini para generación de contenido.

🚀 Uso:
   python scripts/setup_gemini.py

✅ Lo que hace:
   - Muestra instrucciones para obtener API key
   - Crea archivo de configuración de ejemplo
   - Verifica si la API key ya está configurada

🔑 Para obtener API key:
   1. Ve a: https://makersuite.google.com/app/apikey
   2. Haz clic en 'Create API Key'
   3. Copia la API key generada
   4. Agrega la key al archivo .env

📋 Configuración:
   - Modelo: gemini-2.0-flash
   - Max tokens: 2048
   - Temperature: 0.7
""",
        
        "setup_drive.py": """
🔧 setup_drive.py - Configuración de Google Drive

📝 Descripción:
   Configura la integración con Google Drive para gestión de documentos.

🚀 Uso:
   python scripts/setup_drive.py

✅ Lo que hace:
   - Muestra instrucciones para configurar Drive API
   - Crea archivo de configuración de ejemplo
   - Verifica si la configuración ya existe

🔑 Para configurar Drive API:
   1. Ve a: https://console.cloud.google.com/apis/credentials
   2. Crea credenciales OAuth 2.0
   3. Descarga el archivo JSON
   4. Configura la carpeta de Drive

📋 Configuración:
   - Carpeta de Drive para documentos
   - Permisos de acceso
   - Sincronización automática
""",
        
        "setup_secrets.py": """
🔧 setup_secrets.py - Gestión de Secret Manager

📝 Descripción:
   Gestiona los secrets en Google Cloud Secret Manager.

🚀 Uso:
   python scripts/setup_secrets.py

✅ Lo que hace:
   - Lista secrets existentes
   - Crea nuevos secrets si es necesario
   - Actualiza valores de secrets
   - Verifica configuración

📋 Secrets gestionados:
   - legislink-ai-gemini-key
   - legislink-ai-db-password
   - legislink-ai-db-host
   - legislink-ai-db-name
   - legislink-ai-db-user
   - legislink-ai-drive-folder
"""
    }
    
    if script_name in script_help:
        print(script_help[script_name])
    else:
        print(f"❌ No hay ayuda disponible para: {script_name}")
        print("📝 Scripts disponibles:")
        for script in script_help.keys():
            print(f"   - {script}")

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        script_name = sys.argv[1]
        show_script_help(script_name)
    else:
        show_help()

if __name__ == "__main__":
    main() 