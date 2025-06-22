import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manager.sub_agents.crm_agent.agent import create_client, find_client, create_case, find_case
from manager.sub_agents.document_agent.agent import generate_document, review_document
from manager.sub_agents.rag_agent.agent import search_legal_knowledge, add_document_to_knowledge_base
from manager.sub_agents.constitute_agent.agent import validate_constitutional_process, search_constitutional_articles

class TestCRMAgent:
    """Tests para el agente CRM."""
    
    def test_create_client_success(self):
        """Test para crear un cliente exitosamente."""
        data = {
            'nombre': 'Juan Pérez',
            'email': 'juan@test.com',
            'phone': '123456789'
        }
        result = create_client(data)
        assert 'mensaje' in result or 'error' in result
    
    def test_create_client_missing_data(self):
        """Test para crear cliente con datos faltantes."""
        data = {'nombre': 'Juan Pérez'}  # Falta email
        result = create_client(data)
        assert 'error' in result
    
    def test_find_client_success(self):
        """Test para buscar un cliente."""
        data = {'email': 'juan@test.com'}
        result = find_client(data)
        assert isinstance(result, dict)
    
    def test_find_client_missing_email(self):
        """Test para buscar cliente sin email."""
        data = {}
        result = find_client(data)
        assert 'error' in result

class TestDocumentAgent:
    """Tests para el agente de documentos."""
    
    def test_generate_document_success(self):
        """Test para generar un documento."""
        data = {
            'tipo': 'contrato',
            'descripcion': 'Contrato de servicios',
            'puntos': ['Servicios a prestar', 'Pago', 'Duración']
        }
        result = generate_document(data)
        assert isinstance(result, dict)
    
    def test_review_document_success(self):
        """Test para revisar un documento."""
        data = {
            'documento': 'Este es un documento de prueba',
            'tipo_revision': 'general'
        }
        result = review_document(data)
        assert isinstance(result, dict)
    
    def test_review_document_missing_content(self):
        """Test para revisar documento sin contenido."""
        data = {'tipo_revision': 'general'}
        result = review_document(data)
        assert 'error' in result

class TestRAGAgent:
    """Tests para el agente RAG."""
    
    def test_search_legal_knowledge_success(self):
        """Test para búsqueda de conocimiento legal."""
        data = {'pregunta': '¿Qué es un contrato?'}
        result = search_legal_knowledge(data)
        assert isinstance(result, dict)
    
    def test_search_legal_knowledge_missing_question(self):
        """Test para búsqueda sin pregunta."""
        data = {}
        result = search_legal_knowledge(data)
        assert 'error' in result
    
    def test_add_document_to_knowledge_base_success(self):
        """Test para añadir documento a la base de conocimiento."""
        data = {
            'titulo': 'Test Document',
            'contenido': 'Este es un documento de prueba',
            'categoria': 'test'
        }
        result = add_document_to_knowledge_base(data)
        assert isinstance(result, dict)
    
    def test_add_document_missing_data(self):
        """Test para añadir documento con datos faltantes."""
        data = {'titulo': 'Test Document'}  # Falta contenido
        result = add_document_to_knowledge_base(data)
        assert 'error' in result

class TestConstituteAgent:
    """Tests para el agente Constitute."""
    
    def test_validate_constitutional_process_success(self):
        """Test para validar proceso constitucional."""
        data = {
            'proceso': 'derecho a la educación',
            'pais': 'cl'
        }
        result = validate_constitutional_process(data)
        assert isinstance(result, dict)
    
    def test_validate_constitutional_process_missing_data(self):
        """Test para validar proceso sin datos."""
        data = {}
        result = validate_constitutional_process(data)
        assert 'error' in result
    
    def test_search_constitutional_articles_success(self):
        """Test para buscar artículos constitucionales."""
        data = {
            'tema': 'derechos humanos',
            'pais': 'cl'
        }
        result = search_constitutional_articles(data)
        assert isinstance(result, dict)
    
    def test_search_constitutional_articles_missing_topic(self):
        """Test para buscar artículos sin tema."""
        data = {'pais': 'cl'}
        result = search_constitutional_articles(data)
        assert 'error' in result

if __name__ == "__main__":
    pytest.main([__file__]) 