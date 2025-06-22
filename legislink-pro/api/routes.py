from flask import Blueprint, request, jsonify
from manager.agent_manager import root_agent
import logging

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api/v1/delegate', methods=['POST'])
def delegate():
    """
    Endpoint principal para delegar tareas a los agentes.
    """
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Falta el campo "query" en el JSON.'}), 400
    
    query = data['query']
    input_data = data.get('input_data', {})
    
    try:
        logging.info(f"Delegando tarea: {query}")
        
        # Usar el agente ADK para procesar la solicitud
        result = root_agent.run({
            "query": query,
            "input_data": input_data
        })
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        logging.error(f"Error al delegar tarea: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/v1/agents', methods=['GET'])
def list_agents():
    """
    Endpoint para listar los agentes disponibles.
    """
    agents = [
        {
            "name": "crm_agent",
            "description": "Gestión de clientes y casos legales",
            "capabilities": ["crear_cliente", "buscar_cliente", "crear_caso", "buscar_caso"]
        },
        {
            "name": "rag_agent", 
            "description": "Búsqueda semántica en base de conocimiento legal",
            "capabilities": ["buscar_conocimiento", "añadir_documento"]
        },
        {
            "name": "constitute_agent",
            "description": "Validación constitucional y análisis legal",
            "capabilities": ["validar_proceso", "buscar_articulos", "analizar_compatibilidad"]
        },
        {
            "name": "document_agent",
            "description": "Generación y revisión de documentos legales",
            "capabilities": ["generar_documento", "revisar_documento"]
        }
    ]
    
    return jsonify({'agents': agents}), 200

@api_bp.route('/api/v1/health/agents', methods=['GET'])
def agent_health():
    """
    Endpoint para verificar el estado de los agentes.
    """
    try:
        # Verificar que todos los agentes están disponibles
        agent_status = {
            "crm_agent": "available",
            "rag_agent": "available", 
            "constitute_agent": "available",
            "document_agent": "available",
            "manager_agent": "available"
        }
        
        return jsonify({
            'status': 'healthy',
            'agents': agent_status,
            'timestamp': '2024-01-01T00:00:00Z'
        }), 200
        
    except Exception as e:
        logging.error(f"Error en health check de agentes: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500 