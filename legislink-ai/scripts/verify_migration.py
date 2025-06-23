#!/usr/bin/env python3
"""
Script para verificar que la migración de legislink-pro a legislink-ai se ha completado correctamente
"""

import os
import subprocess
import re

class MigrationVerifier:
    def __init__(self):
        self.old_name = "legislink-pro"
        self.new_name = "legislink-ai"
        self.old_display_name = "LegisLink Pro"
        self.new_display_name = "LegisLink AI"
        
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
    
    def check_file_content(self, file_path, expected_patterns, unexpected_patterns=None):
        """Verifica el contenido de un archivo"""
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            all_good = True
            
            # Verificar patrones esperados
            for pattern in expected_patterns:
                if pattern not in content:
                    print(f"❌ Patrón no encontrado en {file_path}: {pattern}")
                    all_good = False
                else:
                    print(f"✅ Patrón encontrado en {file_path}: {pattern}")
            
            # Verificar patrones inesperados
            if unexpected_patterns:
                for pattern in unexpected_patterns:
                    if pattern in content:
                        print(f"❌ Patrón inesperado encontrado en {file_path}: {pattern}")
                        all_good = False
            
            return all_good
        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")
            return False
    
    def verify_google_cloud_project(self):
        """Verifica la configuración del proyecto en Google Cloud"""
        print("\n☁️  Verificando proyecto de Google Cloud...")
        
        # Verificar proyecto actual
        current_project = self.run_command(
            "gcloud config get-value project",
            "Obteniendo proyecto actual"
        )
        
        if current_project == self.new_name:
            print(f"✅ Proyecto configurado correctamente: {current_project}")
        else:
            print(f"❌ Proyecto incorrecto: {current_project} (esperado: {self.new_name})")
            return False
        
        # Verificar que el proyecto existe
        project_exists = self.run_command(
            f"gcloud projects describe {self.new_name}",
            f"Verificando que el proyecto {self.new_name} existe"
        )
        
        if project_exists:
            print(f"✅ Proyecto {self.new_name} existe")
        else:
            print(f"❌ Proyecto {self.new_name} no existe")
            return False
        
        return True
    
    def verify_service_account(self):
        """Verifica el service account"""
        print("\n👤 Verificando service account...")
        
        # Verificar que el service account existe
        sa_exists = self.run_command(
            f"gcloud iam service-accounts describe {self.new_name}-service@{self.new_name}.iam.gserviceaccount.com",
            f"Verificando service account: {self.new_name}-service"
        )
        
        if sa_exists:
            print(f"✅ Service account {self.new_name}-service existe")
        else:
            print(f"❌ Service account {self.new_name}-service no existe")
            return False
        
        # Verificar credenciales
        credentials_path = os.path.expanduser(f"~/{self.new_name}-service-key.json")
        if os.path.exists(credentials_path):
            print(f"✅ Credenciales encontradas: {credentials_path}")
        else:
            print(f"❌ Credenciales no encontradas: {credentials_path}")
            return False
        
        return True
    
    def verify_cloud_sql(self):
        """Verifica Cloud SQL"""
        print("\n🗄️  Verificando Cloud SQL...")
        
        # Verificar instancia
        instance_exists = self.run_command(
            f"gcloud sql instances describe {self.new_name}-db",
            f"Verificando instancia MySQL: {self.new_name}-db"
        )
        
        if instance_exists:
            print(f"✅ Instancia MySQL {self.new_name}-db existe")
        else:
            print(f"❌ Instancia MySQL {self.new_name}-db no existe")
            return False
        
        # Verificar base de datos
        db_exists = self.run_command(
            f"gcloud sql databases describe {self.new_name}_db --instance={self.new_name}-db",
            f"Verificando base de datos: {self.new_name}_db"
        )
        
        if db_exists:
            print(f"✅ Base de datos {self.new_name}_db existe")
        else:
            print(f"❌ Base de datos {self.new_name}_db no existe")
            return False
        
        return True
    
    def verify_memorystore(self):
        """Verifica MemoryStore"""
        print("\n🔴 Verificando MemoryStore...")
        
        redis_exists = self.run_command(
            f"gcloud redis instances describe {self.new_name}-redis --region=us-central1",
            f"Verificando instancia Redis: {self.new_name}-redis"
        )
        
        if redis_exists:
            print(f"✅ Instancia Redis {self.new_name}-redis existe")
            return True
        else:
            print(f"❌ Instancia Redis {self.new_name}-redis no existe")
            return False
    
    def verify_artifact_registry(self):
        """Verifica Artifact Registry"""
        print("\n🐳 Verificando Artifact Registry...")
        
        repo_exists = self.run_command(
            f"gcloud artifacts repositories describe {self.new_name}-repo --location=us-central1",
            f"Verificando repositorio Docker: {self.new_name}-repo"
        )
        
        if repo_exists:
            print(f"✅ Repositorio Docker {self.new_name}-repo existe")
            return True
        else:
            print(f"❌ Repositorio Docker {self.new_name}-repo no existe")
            return False
    
    def verify_secret_manager(self):
        """Verifica Secret Manager"""
        print("\n🔐 Verificando Secret Manager...")
        
        secrets = [
            f"{self.new_name}-gemini-key",
            f"{self.new_name}-db-password",
            f"{self.new_name}-db-host",
            f"{self.new_name}-db-name",
            f"{self.new_name}-db-user",
            f"{self.new_name}-drive-folder"
        ]
        
        all_secrets_exist = True
        
        for secret in secrets:
            secret_exists = self.run_command(
                f"gcloud secrets describe {secret}",
                f"Verificando secret: {secret}"
            )
            
            if secret_exists:
                print(f"✅ Secret {secret} existe")
            else:
                print(f"❌ Secret {secret} no existe")
                all_secrets_exist = False
        
        return all_secrets_exist
    
    def verify_files(self):
        """Verifica que los archivos han sido actualizados correctamente"""
        print("\n📝 Verificando archivos del proyecto...")
        
        # Archivos a verificar
        files_to_check = [
            {
                "path": "env.example",
                "expected": [self.new_name, self.new_display_name],
                "unexpected": [self.old_name, self.old_display_name]
            },
            {
                "path": "README.md",
                "expected": [self.new_name, self.new_display_name],
                "unexpected": [self.old_name, self.old_display_name]
            },
            {
                "path": "CONFIGURATION_GUIDE.md",
                "expected": [self.new_name, self.new_display_name],
                "unexpected": [self.old_name, self.old_display_name]
            },
            {
                "path": "scripts/setup_complete.py",
                "expected": [self.new_name],
                "unexpected": [self.old_name]
            },
            {
                "path": "scripts/update_env.py",
                "expected": [self.new_name],
                "unexpected": [self.old_name]
            },
            {
                "path": "config/settings.py",
                "expected": [self.new_name],
                "unexpected": [self.old_name]
            },
            {
                "path": "frontend/src/locales/en.json",
                "expected": [self.new_display_name],
                "unexpected": [self.old_display_name]
            },
            {
                "path": "frontend/src/locales/es.json",
                "expected": [self.new_display_name],
                "unexpected": [self.old_display_name]
            }
        ]
        
        all_files_good = True
        
        for file_check in files_to_check:
            if not self.check_file_content(
                file_check["path"],
                file_check["expected"],
                file_check["unexpected"]
            ):
                all_files_good = False
        
        return all_files_good
    
    def verify_directory_structure(self):
        """Verifica la estructura de directorios"""
        print("\n📁 Verificando estructura de directorios...")
        
        current_dir = os.getcwd()
        
        if current_dir.endswith(self.new_name):
            print(f"✅ Directorio correcto: {current_dir}")
            return True
        else:
            print(f"❌ Directorio incorrecto: {current_dir}")
            print(f"   Esperado que termine en: {self.new_name}")
            return False
    
    def verify_apis_enabled(self):
        """Verifica que las APIs estén habilitadas"""
        print("\n🔌 Verificando APIs habilitadas...")
        
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
        
        all_apis_enabled = True
        
        for api in apis:
            api_enabled = self.run_command(
                f"gcloud services list --enabled --filter='name:{api}'",
                f"Verificando API: {api}"
            )
            
            if api_enabled and api in api_enabled:
                print(f"✅ API {api} habilitada")
            else:
                print(f"❌ API {api} no habilitada")
                all_apis_enabled = False
        
        return all_apis_enabled
    
    def generate_report(self, results):
        """Genera un reporte de verificación"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE VERIFICACIÓN DE MIGRACIÓN")
        print("=" * 60)
        
        total_checks = len(results)
        passed_checks = sum(1 for result in results.values() if result)
        failed_checks = total_checks - passed_checks
        
        print(f"\n📈 Resumen:")
        print(f"   Total de verificaciones: {total_checks}")
        print(f"   ✅ Exitosas: {passed_checks}")
        print(f"   ❌ Fallidas: {failed_checks}")
        print(f"   📊 Porcentaje de éxito: {(passed_checks/total_checks)*100:.1f}%")
        
        print(f"\n📋 Detalles:")
        for check_name, result in results.items():
            status = "✅ PASÓ" if result else "❌ FALLÓ"
            print(f"   {status} {check_name}")
        
        if failed_checks == 0:
            print(f"\n🎉 ¡Migración completada exitosamente!")
            print(f"   El proyecto {self.new_name} está listo para usar.")
        else:
            print(f"\n⚠️  Se encontraron {failed_checks} problemas.")
            print(f"   Revisa los errores y ejecuta los pasos manualmente si es necesario.")
        
        return failed_checks == 0
    
    def run(self):
        """Ejecuta todas las verificaciones"""
        print("🔍 Iniciando verificación de migración")
        print(f"   Proyecto: {self.old_name} → {self.new_name}")
        print("=" * 60)
        
        results = {}
        
        # Verificaciones de Google Cloud
        results["Google Cloud Project"] = self.verify_google_cloud_project()
        results["Service Account"] = self.verify_service_account()
        results["Cloud SQL"] = self.verify_cloud_sql()
        results["MemoryStore"] = self.verify_memorystore()
        results["Artifact Registry"] = self.verify_artifact_registry()
        results["Secret Manager"] = self.verify_secret_manager()
        results["APIs Habilitadas"] = self.verify_apis_enabled()
        
        # Verificaciones de archivos
        results["Archivos del Proyecto"] = self.verify_files()
        results["Estructura de Directorios"] = self.verify_directory_structure()
        
        # Generar reporte
        success = self.generate_report(results)
        
        if success:
            print(f"\n📝 Próximos pasos:")
            print(f"1. Ejecuta la configuración completa: python scripts/setup_complete.py")
            print(f"2. Actualiza el archivo .env: python scripts/update_env.py")
            print(f"3. Haz push a GitHub para desplegar automáticamente")
            print(f"4. Verifica que la aplicación funcione correctamente")
        
        return success

def main():
    """Función principal"""
    verifier = MigrationVerifier()
    verifier.run()

if __name__ == "__main__":
    main() 