#!/usr/bin/env python3
"""
Script para configurar Secret Manager para LegisLink Pro
"""

import os
import json
from google.cloud import secretmanager

def setup_secrets():
    """Configura los secrets en Secret Manager"""
    
    print("🔐 Configurando Secret Manager...")
    
    # Configuración del proyecto
    PROJECT_ID = "legislink-pro"
    
    # Crear cliente de Secret Manager
    client = secretmanager.SecretManagerServiceClient()
    
    # Lista de secrets a crear
    secrets = [
        {
            "secret_id": "legislink-gemini-key",
            "description": "API key para Gemini AI"
        },
        {
            "secret_id": "legislink-db-password",
            "description": "Contraseña de la base de datos MySQL"
        },
        {
            "secret_id": "legislink-db-host",
            "description": "Host de la base de datos Cloud SQL"
        },
        {
            "secret_id": "legislink-db-name",
            "description": "Nombre de la base de datos"
        },
        {
            "secret_id": "legislink-db-user",
            "description": "Usuario de la base de datos"
        },
        {
            "secret_id": "legislink-drive-folder",
            "description": "ID de la carpeta de Google Drive"
        }
    ]
    
    created_secrets = []
    
    for secret_info in secrets:
        secret_id = secret_info["secret_id"]
        parent = f"projects/{PROJECT_ID}"
        secret_path = f"{parent}/secrets/{secret_id}"
        
        try:
            # Verificar si el secret ya existe
            client.get_secret(request={"name": secret_path})
            print(f"✅ Secret '{secret_id}' ya existe")
            created_secrets.append(secret_id)
            
        except Exception:
            # Crear el secret
            try:
                secret = client.create_secret(
                    request={
                        "parent": parent,
                        "secret_id": secret_id,
                        "secret": {"replication": {"automatic": {}}}
                    }
                )
                
                print(f"✅ Secret '{secret_id}' creado: {secret.name}")
                created_secrets.append(secret_id)
                
            except Exception as e:
                print(f"❌ Error creando secret '{secret_id}': {e}")
    
    # Crear archivo de configuración
    config = {
        "project_id": PROJECT_ID,
        "secrets": created_secrets,
        "instructions": [
            "Para agregar valores a los secrets:",
            "gcloud secrets versions add SECRET_ID --data-file=archivo.txt",
            "o",
            "echo -n 'valor' | gcloud secrets versions add SECRET_ID --data-file=-"
        ]
    }
    
    with open("secrets_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuración de secrets guardada en secrets_config.json")
    
    return created_secrets

def add_secret_value(secret_id, value):
    """Agrega un valor a un secret"""
    
    try:
        PROJECT_ID = "legislink-pro"
        client = secretmanager.SecretManagerServiceClient()
        
        parent = f"projects/{PROJECT_ID}/secrets/{secret_id}"
        
        # Agregar nueva versión del secret
        response = client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": value.encode("UTF-8")}
            }
        )
        
        print(f"✅ Valor agregado al secret '{secret_id}': {response.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error agregando valor al secret '{secret_id}': {e}")
        return False

def list_secrets():
    """Lista todos los secrets del proyecto"""
    
    try:
        PROJECT_ID = "legislink-pro"
        client = secretmanager.SecretManagerServiceClient()
        
        print("📋 Listando secrets...")
        
        # Usar gcloud para listar secrets
        import subprocess
        result = subprocess.run([
            "gcloud", "secrets", "list", 
            "--project=legislink-pro"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("❌ Error listando secrets")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_secrets()
    list_secrets()
