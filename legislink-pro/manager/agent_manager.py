from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from manager.sub_agents.crm_agent.agent import crm_agent
from manager.sub_agents.document_agent.agent import document_agent
from manager.sub_agents.rag_agent.agent import rag_agent
from manager.sub_agents.constitute_agent.agent import constitute_agent
import logging

def get_current_time():
    """Herramienta para obtener la hora actual."""
    from datetime import datetime
    return {"current_time": datetime.now().isoformat()}

def route_request(input_data: dict) -> dict:
    """
    Herramienta para enrutar solicitudes a los agentes apropiados.
    """
    query = input_data.get('query', '').lower()
    
    if any(keyword in query for keyword in ['cliente', 'crm', 'caso', 'crear', 'buscar']):
        return {"agent": "crm_agent", "reason": "Solicitud relacionada con gestión de clientes y casos"}
    elif any(keyword in query for keyword in ['buscar documento', 'rag', 'pregunta', 'ley', 'conocimiento']):
        return {"agent": "rag_agent", "reason": "Solicitud de búsqueda en base de conocimiento legal"}
    elif any(keyword in query for keyword in ['constitución', 'valida', 'constitucional']):
        return {"agent": "constitute_agent", "reason": "Solicitud de validación constitucional"}
    elif any(keyword in query for keyword in ['genera', 'borrador', 'documento', 'redacta']):
        return {"agent": "document_agent", "reason": "Solicitud de generación de documentos"}
    else:
        return {"agent": "rag_agent", "reason": "Solicitud general, usando RAG como fallback"}

def handle_error(error_info: dict) -> dict:
    """
    Herramienta para manejar errores de los agentes.
    """
    logging.error(f"Error en agente: {error_info}")
    return {
        "error": True,
        "message": "Ocurrió un error al procesar la solicitud",
        "details": error_info.get('details', 'Error desconocido'),
        "suggestion": "Intenta reformular tu consulta o contacta soporte"
    }

# Crear el agente manager principal usando ADK
root_agent = Agent(
    name="legislink_manager",
    model="gemini-2.0-flash",
    description="Agente orquestador principal de LegisLink Pro que coordina todos los sub-agentes especializados.",
    instruction="""
    Eres el agente orquestador principal de LegisLink Pro, una plataforma multiagente para automatización legal.
    
    Tu responsabilidad es:
    1. Analizar las solicitudes de los usuarios
    2. Determinar qué agente especializado es el más adecuado para cada tarea
    3. Coordinar la ejecución de los sub-agentes
    4. Manejar errores y proporcionar respuestas coherentes
    
    Agentes disponibles:
    - crm_agent: Gestión de clientes y casos legales
    - rag_agent: Búsqueda semántica en base de conocimiento legal
    - constitute_agent: Validación constitucional y análisis legal
    - document_agent: Generación y revisión de documentos legales
    
    Siempre:
    - Usa la herramienta route_request para determinar el agente apropiado
    - Proporciona respuestas claras y útiles
    - Maneja errores de forma elegante
    - Mantén el contexto de la conversación
    """,
    sub_agents=[crm_agent, rag_agent, constitute_agent, document_agent],
    tools=[
        AgentTool(route_request),
        get_current_time,
        AgentTool(handle_error),
    ],
) 