#!/usr/bin/env python3
"""
Script para renombrar el proyecto de legislink-pro a legislink-ai
Actualiza todos los archivos y configuraciones necesarias
"""

import os
import re
import subprocess
import shutil
from pathlib import Path

class ProjectRenamer:
    def __init__(self):
        self.old_name = "legislink-pro"
        self.new_name = "legislink-ai"
        self.old_display_name = "LegisLink Pro"
        self.new_display_name = "LegisLink AI"
        
    def run_command(self, command, description, check=True):
        """Ejecuta un comando y maneja errores"""
        print(f"🔄 {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description} - Exitoso")
                return result.stdout.strip()
            else:
                print(f"❌ {description} - Falló: {result.stderr}")
                if check:
                    raise Exception(f"Comando falló: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")
            if check:
                raise
            return None
    
    def update_file_content(self, file_path, old_text, new_text):
        """Actualiza el contenido de un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar texto
            updated_content = content.replace(old_text, new_text)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Actualizado: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error actualizando {file_path}: {e}")
            return False
    
    def update_files(self):
        """Actualiza todos los archivos del proyecto"""
        print("\n📝 Actualizando archivos del proyecto...")
        
        # Lista de archivos a actualizar
        files_to_update = [
            "env.example",
            "README.md",
            "CONFIGURATION_GUIDE.md",
            "scripts/setup_complete.py",
            "scripts/setup_vertex_ai.py",
            "scripts/setup_gemini.py",
            "scripts/setup_drive.py",
            "scripts/setup_secrets.py",
            "scripts/update_env.py",
            "config/settings.py",
            "api/main.py",
            "frontend/package.json",
            "frontend/src/locales/en.json",
            "frontend/src/locales/es.json",
            "cloudbuild.yaml",
            ".github/workflows/deploy.yml",
            "../docker-compose.yml"
        ]
        
        # Reemplazos a realizar
        replacements = [
            (self.old_name, self.new_name),
            (self.old_display_name, self.new_display_name),
            ("legislink-db.legislink-pro", f"legislink-db.{self.new_name}"),
            ("legislink-service@legislink-pro", f"legislink-service@{self.new_name}"),
            ("legislink-service-key.json", f"{self.new_name}-service-key.json"),
            ("legislink_db", f"{self.new_name}_db"),
            ("legislink-db", f"{self.new_name}-db"),
            ("legislink-redis", f"{self.new_name}-redis"),
            ("legislink-repo", f"{self.new_name}-repo"),
            ("legislink-backend", f"{self.new_name}-backend"),
            ("legislink-frontend", f"{self.new_name}-frontend"),
            ("legislink_net", f"{self.new_name}_net"),
            ("projects/legislink-pro", f"projects/{self.new_name}"),
            ("legislink-gemini-key", f"{self.new_name}-gemini-key"),
            ("legislink-db-password", f"{self.new_name}-db-password"),
            ("legislink-db-host", f"{self.new_name}-db-host"),
            ("legislink-db-name", f"{self.new_name}-db-name"),
            ("legislink-db-user", f"{self.new_name}-db-user"),
            ("legislink-drive-folder", f"{self.new_name}-drive-folder"),
            ("legislink-legal-docs", f"{self.new_name}-legal-docs"),
            ("legislink-search-endpoint", f"{self.new_name}-search-endpoint"),
            ("legislink-legal-docs-deployed", f"{self.new_name}-legal-docs-deployed"),
            ("legislink-docs", f"{self.new_name}-docs")
        ]
        
        for file_path in files_to_update:
            if os.path.exists(file_path):
                for old_text, new_text in replacements:
                    self.update_file_content(file_path, old_text, new_text)
            else:
                print(f"⚠️  Archivo no encontrado: {file_path}")
    
    def update_google_cloud_project(self):
        """Actualiza el proyecto en Google Cloud"""
        print("\n☁️  Actualizando proyecto en Google Cloud...")
        
        # Crear nuevo proyecto
        self.run_command(
            f"gcloud projects create {self.new_name} --name='{self.new_display_name}'",
            f"Creando nuevo proyecto: {self.new_name}",
            check=False
        )
        
        # Configurar nuevo proyecto
        self.run_command(
            f"gcloud config set project {self.new_name}",
            f"Configurando proyecto: {self.new_name}"
        )
        
        # Habilitar facturación (manual)
        print(f"📝 IMPORTANTE: Habilita la facturación para el proyecto {self.new_name}")
        print(f"   Ve a: https://console.cloud.google.com/billing/projects/{self.new_name}")
    
    def update_docker_repository(self):
        """Actualiza el repositorio de Docker"""
        print("\n🐳 Actualizando repositorio de Docker...")
        
        # Crear nuevo repositorio
        self.run_command(
            f"gcloud artifacts repositories create {self.new_name}-repo --repository-format=docker --location=us-central1 --description='Docker repository for {self.new_display_name}'",
            f"Creando repositorio Docker: {self.new_name}-repo",
            check=False
        )
        
        # Configurar Docker
        self.run_command(
            "gcloud auth configure-docker us-central1-docker.pkg.dev",
            "Configurando Docker para nuevo repositorio"
        )
    
    def update_service_account(self):
        """Actualiza el service account"""
        print("\n👤 Actualizando service account...")
        
        # Crear nuevo service account
        self.run_command(
            f"gcloud iam service-accounts create {self.new_name}-service --display-name='{self.new_display_name} Service Account'",
            f"Creando service account: {self.new_name}-service",
            check=False
        )
        
        # Asignar roles
        roles = [
            "roles/cloudsql.client",
            "roles/redis.admin",
            "roles/aiplatform.user",
            "roles/drive.file",
            "roles/secretmanager.secretAccessor",
            "roles/storage.objectViewer",
            "roles/logging.logWriter",
            "roles/monitoring.metricWriter"
        ]
        
        for role in roles:
            self.run_command(
                f"gcloud projects add-iam-policy-binding {self.new_name} --member='serviceAccount:{self.new_name}-service@{self.new_name}.iam.gserviceaccount.com' --role='{role}'",
                f"Asignando rol: {role}"
            )
        
        # Crear nuevas credenciales
        credentials_path = os.path.expanduser(f"~/{self.new_name}-service-key.json")
        self.run_command(
            f"gcloud iam service-accounts keys create {credentials_path} --iam-account={self.new_name}-service@{self.new_name}.iam.gserviceaccount.com",
            f"Creando credenciales: {credentials_path}"
        )
    
    def update_cloud_sql(self):
        """Actualiza Cloud SQL"""
        print("\n��️  Actualizando Cloud SQL...")
        
        # Crear nueva instancia
        self.run_command(
            f"gcloud sql instances create {self.new_name}-db --database-version=MYSQL_8_0 --tier=db-f1-micro --region=us-central1 --root-password=LegisLink2024! --storage-type=SSD --storage-size=10GB",
            f"Creando instancia MySQL: {self.new_name}-db",
            check=False
        )
        
        # Crear base de datos
        self.run_command(
            f"gcloud sql databases create {self.new_name}_db --instance={self.new_name}-db",
            f"Creando base de datos: {self.new_name}_db",
            check=False
        )
        
        # Crear usuario
        self.run_command(
            f"gcloud sql users create {self.new_name} --instance={self.new_name}-db --password=LegisLink2024!",
            f"Creando usuario: {self.new_name}",
            check=False
        )
    
    def update_memorystore(self):
        """Actualiza MemoryStore"""
        print("\n🔴 Actualizando MemoryStore...")
        
        self.run_command(
            f"gcloud redis instances create {self.new_name}-redis --size=1 --region=us-central1 --redis-version=redis_6_x",
            f"Creando instancia Redis: {self.new_name}-redis",
            check=False
        )
    
    def update_secret_manager(self):
        """Actualiza Secret Manager"""
        print("\n🔐 Actualizando Secret Manager...")
        
        secrets = [
            f"{self.new_name}-gemini-key",
            f"{self.new_name}-db-password",
            f"{self.new_name}-db-host",
            f"{self.new_name}-db-name",
            f"{self.new_name}-db-user",
            f"{self.new_name}-drive-folder"
        ]
        
        for secret in secrets:
            self.run_command(
                f"gcloud secrets create {secret} --replication-policy='automatic'",
                f"Creando secret: {secret}",
                check=False
            )
    
    def update_directory_structure(self):
        """Actualiza la estructura de directorios"""
        print("\n📁 Actualizando estructura de directorios...")
        
        # Renombrar directorio actual
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        new_dir = os.path.join(parent_dir, self.new_name)
        
        if current_dir.endswith(self.old_name):
            try:
                shutil.move(current_dir, new_dir)
                print(f"✅ Directorio renombrado: {current_dir} -> {new_dir}")
                print(f"📝 IMPORTANTE: Navega al nuevo directorio: cd {new_dir}")
            except Exception as e:
                print(f"❌ Error renombrando directorio: {e}")
                print("📝 Renombra manualmente el directorio si es necesario")
    
    def show_migration_instructions(self):
        """Muestra instrucciones de migración"""
        print("\n" + "=" * 60)
        print("🎉 ¡Renombrado del proyecto completado!")
        print("=" * 60)
        
        print(f"\n📋 Cambios realizados:")
        print(f"   - Proyecto: {self.old_name} -> {self.new_name}")
        print(f"   - Nombre: {self.old_display_name} -> {self.new_display_name}")
        print(f"   - Service Account: {self.new_name}-service@{self.new_name}.iam.gserviceaccount.com")
        print(f"   - Base de datos: {self.new_name}_db")
        print(f"   - Redis: {self.new_name}-redis")
        print(f"   - Repositorio Docker: {self.new_name}-repo")
        
        print(f"\n📝 Próximos pasos:")
        print(f"1. Navega al nuevo directorio: cd ../{self.new_name}")
        print(f"2. Habilita la facturación para el proyecto {self.new_name}")
        print(f"3. Ejecuta la configuración completa: python scripts/setup_complete.py")
        print(f"4. Actualiza el archivo .env: python scripts/update_env.py")
        print(f"5. Haz push a GitHub para desplegar automáticamente")
        
        print(f"\n🔗 URLs importantes:")
        print(f"   - Google Cloud Console: https://console.cloud.google.com/home/dashboard?project={self.new_name}")
        print(f"   - Facturación: https://console.cloud.google.com/billing/projects/{self.new_name}")
        print(f"   - APIs: https://console.cloud.google.com/apis/dashboard?project={self.new_name}")
    
    def run(self):
        """Ejecuta el proceso completo de renombrado"""
        print("🚀 Iniciando renombrado del proyecto")
        print(f"   De: {self.old_name} ({self.old_display_name})")
        print(f"   A: {self.new_name} ({self.new_display_name})")
        print("=" * 60)
        
        try:
            # Actualizar archivos del proyecto
            self.update_files()
            
            # Actualizar Google Cloud
            self.update_google_cloud_project()
            self.update_docker_repository()
            self.update_service_account()
            self.update_cloud_sql()
            self.update_memorystore()
            self.update_secret_manager()
            
            # Actualizar estructura de directorios
            self.update_directory_structure()
            
            # Mostrar instrucciones
            self.show_migration_instructions()
            
        except Exception as e:
            print(f"\n❌ Error durante el renombrado: {e}")
            print("📝 Revisa los errores y ejecuta los pasos manualmente si es necesario")

def main():
    """Función principal"""
    renamer = ProjectRenamer()
    renamer.run()

if __name__ == "__main__":
    main()
