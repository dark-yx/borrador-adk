#!/usr/bin/env python3
"""
Script para configurar Google Drive API para LegisLink AI
"""

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Scopes necesarios para Google Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

def setup_drive_api():
    """Configura la API de Google Drive"""
    
    print("📁 Configurando Google Drive API...")
    
    creds = None
    
    # Verificar si ya existen credenciales guardadas
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Si no hay credenciales válidas, solicitar autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Crear archivo de configuración OAuth
            client_config = {
                "installed": {
                    "client_id": "TU_CLIENT_ID",
                    "project_id": "legislink-ai",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": "TU_CLIENT_SECRET",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                }
            }
            
            with open('credentials.json', 'w') as f:
                json.dump(client_config, f, indent=2)
            
            print("📝 Para configurar Google Drive API:")
            print("1. Ve a: https://console.cloud.google.com/apis/credentials")
            print("2. Crea credenciales OAuth 2.0")
            print("3. Descarga el archivo JSON")
            print("4. Renómbralo como 'credentials.json' en este directorio")
            print("5. Ejecuta este script nuevamente")
            
            return False
        
        # Guardar credenciales para uso futuro
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Crear servicio de Drive
    try:
        service = build('drive', 'v3', credentials=creds)
        
        # Crear carpeta para LegisLink
        folder_metadata = {
            'name': 'LegisLink Documents',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        folder = service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        
        folder_id = folder.get('id')
        
        print(f"✅ Carpeta de Drive creada: {folder_id}")
        
        # Guardar configuración
        config = {
            "drive_folder_id": folder_id,
            "service_account_email": "legislink-service@legislink-ai.iam.gserviceaccount.com"
        }
        
        with open("drive_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuración de Drive guardada en drive_config.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error configurando Google Drive: {e}")
        return False

def test_drive_connection():
    """Prueba la conexión con Google Drive"""
    
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        # Usar credenciales del service account
        credentials = service_account.Credentials.from_service_account_file(
            '~/legislink-ai-service-key.json',
            scopes=SCOPES
        )
        
        service = build('drive', 'v3', credentials=credentials)
        
        # Listar archivos (prueba simple)
        results = service.files().list(pageSize=10).execute()
        
        print("✅ Conexión con Google Drive exitosa")
        print(f"Archivos encontrados: {len(results.get('files', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectando con Google Drive: {e}")
        return False

if __name__ == "__main__":
    setup_drive_api() 