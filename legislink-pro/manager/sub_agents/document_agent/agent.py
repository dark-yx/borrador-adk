from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from typing import Dict, Any
from services.google_apis import upload_to_drive
import datetime
import google.generativeai as genai
from config.settings import settings

# Configurar Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_document(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera un documento legal basado en las especificaciones proporcionadas.
    """
    tipo = input_data.get('tipo', 'documento_legal')
    puntos = input_data.get('puntos', [])
    descripcion = input_data.get('descripcion', '')
    
    # Generar el documento usando Gemini
    prompt = f"""
    Eres un abogado experto en redacción de documentos legales.
    
    Necesitas generar un documento de tipo: {tipo}
    
    Descripción: {descripcion}
    
    Puntos clave a incluir:
    {chr(10).join([f"- {punto}" for punto in puntos]) if puntos else "- Documento legal estándar"}
    
    Genera un documento legal completo, profesional y bien estructurado en español.
    Incluye todas las cláusulas necesarias y lenguaje legal apropiado.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        documento_generado = response.text
        
        # Guardar en Google Drive
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{tipo}_{timestamp}.txt"
        
        upload_result = upload_to_drive(file_name, documento_generado)
        
        return {
            "documento_generado": documento_generado,
            "google_drive_resultado": upload_result,
            "tipo_documento": tipo,
            "timestamp": timestamp
        }
        
    except Exception as e:
        return {"error": f"Error al generar el documento: {str(e)}"}

def review_document(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Revisa y mejora un documento legal existente.
    """
    documento = input_data.get('documento', '')
    tipo_revision = input_data.get('tipo_revision', 'general')
    
    if not documento:
        return {"error": "No se proporcionó un documento para revisar."}
    
    prompt = f"""
    Eres un abogado experto en revisión de documentos legales.
    
    Revisa el siguiente documento legal y mejóralo según el tipo de revisión solicitado: {tipo_revision}
    
    Documento a revisar:
    {documento}
    
    Proporciona:
    1. El documento mejorado
    2. Lista de cambios realizados
    3. Recomendaciones adicionales
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        revision = response.text
        
        return {
            "documento_revisado": revision,
            "tipo_revision": tipo_revision,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": f"Error al revisar el documento: {str(e)}"}

# Crear el agente de documentos usando ADK
document_agent = Agent(
    name="document_agent",
    model="gemini-2.0-flash",
    description="Agente especializado en la generación y revisión de documentos legales.",
    instruction="""
    Eres un asistente legal experto en la redacción y revisión de documentos legales.
    
    Puedes:
    1. Generar documentos legales completos basados en especificaciones
    2. Revisar y mejorar documentos legales existentes
    3. Guardar automáticamente los documentos en Google Drive
    
    Siempre genera documentos profesionales, bien estructurados y con lenguaje legal apropiado.
    Incluye todas las cláusulas necesarias y asegúrate de que el documento sea legalmente válido.
    """,
    tools=[
        generate_document,
        review_document,
    ],
) 