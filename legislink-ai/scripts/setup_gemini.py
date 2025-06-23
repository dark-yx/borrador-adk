#!/usr/bin/env python3
"""
Script para configurar Gemini API para LegisLink AI
"""

import os
import requests
import json

def setup_gemini_api():
    """Configura la API de Gemini"""
    
    print("🔑 Configurando Gemini API...")
    
    # URL para obtener API key
    gemini_url = "https://makersuite.google.com/app/apikey"
    
    print(f"📝 Para obtener tu API key de Gemini:")
    print(f"1. Ve a: {gemini_url}")
    print("2. Haz clic en 'Create API Key'")
    print("3. Copia la API key generada")
    print("4. Agrega la key al archivo .env")
    
    # Crear archivo de configuración de ejemplo
    config_example = {
        "gemini_api_key": "TU_API_KEY_AQUI",
        "model": "gemini-2.0-flash",
        "max_tokens": 2048,
        "temperature": 0.7
    }
    
    with open("gemini_config_example.json", "w") as f:
        json.dump(config_example, f, indent=2)
    
    print("✅ Archivo de configuración de ejemplo creado: gemini_config_example.json")
    
    # Verificar si ya existe la API key
    if os.getenv("GEMINI_API_KEY"):
        print("✅ GEMINI_API_KEY ya está configurada en las variables de entorno")
        return True
    else:
        print("⚠️  GEMINI_API_KEY no está configurada")
        return False

def test_gemini_connection(api_key):
    """Prueba la conexión con Gemini API"""
    
    try:
        import google.generativeai as genai
        
        # Configurar la API
        genai.configure(api_key=api_key)
        
        # Crear modelo
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prueba simple
        response = model.generate_content("Hola, ¿cómo estás?")
        
        print("✅ Conexión con Gemini API exitosa")
        print(f"Respuesta de prueba: {response.text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectando con Gemini API: {e}")
        return False

if __name__ == "__main__":
    setup_gemini_api() 