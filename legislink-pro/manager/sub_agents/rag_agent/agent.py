import json
import numpy as np
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from typing import Dict, Any, List
from config.settings import settings
from services.google_apis import query_vector_search

# Configure the generative AI model
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
else:
    print("Advertencia: No se encontró la GEMINI_API_KEY. El RAGAgent no funcionará.")

# --- Helper function for similarity search ---
def cosine_similarity(v1, v2):
    """Calcula la similitud coseno entre dos vectores."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def search_legal_knowledge(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Realiza búsqueda semántica en la base de conocimiento legal usando RAG.
    """
    pregunta = input_data.get('pregunta', '')
    index_endpoint_id = settings.VERTEX_AI_INDEX_ENDPOINT_ID
    
    if not pregunta:
        return {"error": "No se proporcionó ninguna pregunta."}
    if not index_endpoint_id:
        return {"error": "El ID del endpoint de índice de Vertex AI no está configurado."}

    try:
        # 1. Generar embedding para la pregunta
        model = genai.GenerativeModel('gemini-2.0-flash')
        result = genai.embed_content(
            model='models/text-embedding-004',
            content=pregunta,
            task_type="RETRIEVAL_QUERY"
        )
        question_embedding = result['embedding']

        # 2. Encontrar los chunks más relevantes usando Vertex AI
        neighbors = query_vector_search(
            index_endpoint_id=index_endpoint_id,
            query_embedding=question_embedding,
            num_neighbors=5
        )
        
        if "error" in neighbors:
            return {"error": f"Error al consultar Vertex AI: {neighbors['error']}"}

        # 3. Extraer contexto de los vecinos más cercanos
        contexto = _extract_context_from_neighbors(neighbors)

        # 4. Generar respuesta aumentada con el contexto
        prompt = f"""
        Rol: Eres un asistente legal experto. Responde la pregunta basándote únicamente en el contexto legal proporcionado.
        
        Contexto Legal Recuperado de la Base de Conocimiento:
        ---
        {contexto}
        ---
        
        Pregunta: {pregunta}
        
        Respuesta:
        """
        
        response = model.generate_content(prompt)
        respuesta_generada = response.text

        return {
            "respuesta": respuesta_generada, 
            "contexto_usado": contexto,
            "pregunta_original": pregunta,
            "num_resultados": len(neighbors[0]) if neighbors and neighbors[0] else 0
        }
        
    except Exception as e:
        return {"error": f"Error en la búsqueda RAG: {str(e)}"}

def add_document_to_knowledge_base(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Añade un nuevo documento a la base de conocimiento legal.
    """
    titulo = input_data.get('titulo', '')
    contenido = input_data.get('contenido', '')
    categoria = input_data.get('categoria', 'general')
    
    if not titulo or not contenido:
        return {"error": "Título y contenido son requeridos para añadir un documento."}
    
    try:
        # Generar embedding para el contenido
        result = genai.embed_content(
            model='models/text-embedding-004',
            content=contenido,
            task_type="RETRIEVAL_DOCUMENT"
        )
        document_embedding = result['embedding']
        
        # Aquí se añadiría la lógica para insertar en Vertex AI
        # Por ahora simulamos la inserción
        return {
            "mensaje": f"Documento '{titulo}' añadido a la base de conocimiento",
            "categoria": categoria,
            "embedding_generado": True
        }
        
    except Exception as e:
        return {"error": f"Error al añadir documento: {str(e)}"}

def _extract_context_from_neighbors(neighbors_response):
    """Extrae el contenido de los vecinos más cercanos."""
    if not neighbors_response or not neighbors_response[0]:
        return "No se encontró contexto relevante en la base de conocimiento."
    
    context = []
    for neighbor in neighbors_response[0]:
        context.append(f"Documento relevante (ID: {neighbor.id}, similitud: {1 - neighbor.distance:.4f})")
    
    return "\n".join(context)

# Crear el agente RAG usando ADK
rag_agent = Agent(
    name="rag_agent",
    model="gemini-2.0-flash",
    description="Agente especializado en búsqueda semántica y recuperación de información legal usando RAG.",
    instruction="""
    Eres un asistente legal experto en búsqueda semántica de información legal.
    
    Puedes:
    1. Buscar información en la base de conocimiento legal usando RAG
    2. Añadir nuevos documentos a la base de conocimiento
    3. Proporcionar respuestas precisas basadas en documentos legales relevantes
    
    Siempre basa tus respuestas en el contexto legal recuperado y cita las fuentes cuando sea posible.
    Si no encuentras información relevante, indícalo claramente.
    """,
    tools=[
        search_legal_knowledge,
        add_document_to_knowledge_base,
    ],
) 