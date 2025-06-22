import requests
import json
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from typing import Dict, Any
from services.cache import redis_client
from config.settings import settings

CONSTITUTE_API_URL = "https://www.constituteproject.org/service/"

def validate_constitutional_process(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida un proceso legal contra la constitución del país especificado.
    """
    proceso_legal = input_data.get('proceso', '')
    pais = input_data.get('pais', 'cl')  # ISO 3166-1 alpha-2, ej: cl, mx, co

    if not proceso_legal:
        return {"error": "No se proporcionó un proceso legal para validar."}

    # Buscar en caché primero
    cache_key = f"constitute:{pais}:{proceso_legal}"
    cached_result = redis_client.get(cache_key)
    
    if cached_result:
        return json.loads(cached_result)

    try:
        # Obtener el ID de la constitución actual del país
        cons_response = requests.get(
            f"{CONSTITUTE_API_URL}constitutions", 
            params={'country_code': pais, 'lang': 'es'}
        )
        cons_response.raise_for_status()
        cons_id = cons_response.json().get('data', [{}])[0].get('id')

        if not cons_id:
            return {"error": f"No se encontró una constitución para el código de país '{pais}'."}

        # Buscar el query en los tópicos de esa constitución
        search_params = {'key': proceso_legal, 'cons_id': cons_id}
        response = requests.get(
            f"{CONSTITUTE_API_URL}sectionstopicsearch", 
            params=search_params
        )
        response.raise_for_status()
        
        api_result = response.json()
        
        # Analizar y formatear el resultado
        articulos_relevantes = []
        if api_result.get('success') and api_result.get('count', 0) > 0:
            for item in api_result['data']:
                articulos_relevantes.append({
                    "articulo": item.get('section_title', 'N/A'),
                    "texto": item.get('section_text', 'N/A'),
                    "url": item.get('url', '#')
                })

        result = {
            "proceso_validado": proceso_legal,
            "pais_constitucion": pais.upper(),
            "es_compatible": len(articulos_relevantes) > 0,
            "articulos_relevantes": articulos_relevantes,
            "confidence_score": api_result.get('count', 0)
        }
        
        # Guardar en caché por 1 hora
        redis_client.set(cache_key, json.dumps(result), ex=3600)
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Error en la llamada a la API de Constitute: {str(e)}"}

def search_constitutional_articles(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Busca artículos constitucionales específicos por tema o palabra clave.
    """
    tema = input_data.get('tema', '')
    pais = input_data.get('pais', 'cl')
    
    if not tema:
        return {"error": "No se proporcionó un tema para buscar."}
    
    try:
        # Obtener el ID de la constitución
        cons_response = requests.get(
            f"{CONSTITUTE_API_URL}constitutions", 
            params={'country_code': pais, 'lang': 'es'}
        )
        cons_response.raise_for_status()
        cons_id = cons_response.json().get('data', [{}])[0].get('id')

        if not cons_id:
            return {"error": f"No se encontró una constitución para el país '{pais}'."}

        # Buscar artículos por tema
        search_params = {'key': tema, 'cons_id': cons_id}
        response = requests.get(
            f"{CONSTITUTE_API_URL}sectionstopicsearch", 
            params=search_params
        )
        response.raise_for_status()
        
        api_result = response.json()
        
        articulos = []
        if api_result.get('success') and api_result.get('count', 0) > 0:
            for item in api_result['data']:
                articulos.append({
                    "titulo": item.get('section_title', 'N/A'),
                    "contenido": item.get('section_text', 'N/A'),
                    "url": item.get('url', '#'),
                    "relevancia": "alta" if tema.lower() in item.get('section_text', '').lower() else "media"
                })

        return {
            "tema_buscado": tema,
            "pais": pais.upper(),
            "articulos_encontrados": len(articulos),
            "articulos": articulos
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al buscar artículos constitucionales: {str(e)}"}

def analyze_constitutional_compatibility(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza la compatibilidad de un texto legal con la constitución.
    """
    texto_legal = input_data.get('texto', '')
    pais = input_data.get('pais', 'cl')
    
    if not texto_legal:
        return {"error": "No se proporcionó un texto legal para analizar."}
    
    # Extraer palabras clave del texto para buscar en la constitución
    palabras_clave = texto_legal.split()[:10]  # Primeras 10 palabras como palabras clave
    
    try:
        # Obtener el ID de la constitución
        cons_response = requests.get(
            f"{CONSTITUTE_API_URL}constitutions", 
            params={'country_code': pais, 'lang': 'es'}
        )
        cons_response.raise_for_status()
        cons_id = cons_response.json().get('data', [{}])[0].get('id')

        if not cons_id:
            return {"error": f"No se encontró una constitución para el país '{pais}'."}

        # Buscar artículos relevantes
        articulos_relevantes = []
        for palabra in palabras_clave:
            if len(palabra) > 3:  # Solo palabras de más de 3 caracteres
                search_params = {'key': palabra, 'cons_id': cons_id}
                response = requests.get(
                    f"{CONSTITUTE_API_URL}sectionstopicsearch", 
                    params=search_params
                )
                response.raise_for_status()
                
                api_result = response.json()
                if api_result.get('success') and api_result.get('count', 0) > 0:
                    for item in api_result['data'][:2]:  # Solo los primeros 2 resultados
                        articulos_relevantes.append({
                            "palabra_clave": palabra,
                            "articulo": item.get('section_title', 'N/A'),
                            "texto": item.get('section_text', 'N/A'),
                            "url": item.get('url', '#')
                        })

        # Eliminar duplicados
        articulos_unicos = []
        seen = set()
        for articulo in articulos_relevantes:
            key = (articulo['palabra_clave'], articulo['articulo'])
            if key not in seen:
                seen.add(key)
                articulos_unicos.append(articulo)

        return {
            "texto_analizado": texto_legal[:200] + "..." if len(texto_legal) > 200 else texto_legal,
            "pais_constitucion": pais.upper(),
            "palabras_clave_analizadas": palabras_clave,
            "articulos_relevantes": articulos_unicos,
            "nivel_compatibilidad": "alta" if len(articulos_unicos) > 5 else "media" if len(articulos_unicos) > 2 else "baja"
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al analizar compatibilidad constitucional: {str(e)}"}

# Crear el agente Constitute usando ADK
constitute_agent = Agent(
    name="constitute_agent",
    model="gemini-2.0-flash",
    description="Agente especializado en validación constitucional y análisis de compatibilidad legal.",
    instruction="""
    Eres un asistente legal experto en derecho constitucional y validación de procesos legales.
    
    Puedes:
    1. Validar procesos legales contra constituciones nacionales
    2. Buscar artículos constitucionales específicos por tema
    3. Analizar la compatibilidad de textos legales con la constitución
    4. Proporcionar referencias a artículos constitucionales relevantes
    
    Siempre especifica el país de la constitución que estás consultando y proporciona enlaces a los artículos relevantes.
    Si no encuentras información constitucional relevante, indícalo claramente.
    """,
    tools=[
        validate_constitutional_process,
        search_constitutional_articles,
        analyze_constitutional_compatibility,
    ],
) 