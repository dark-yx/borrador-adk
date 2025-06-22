import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestAPIEndpoints:
    """Tests para los endpoints de la API."""
    
    def test_health_check(self, client):
        """Test para el endpoint de health check."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
    
    def test_redis_test(self, client):
        """Test para el endpoint de prueba de Redis."""
        response = client.get('/api/redis-test')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'redis_value' in data or 'error' in data
    
    def test_delegate_missing_query(self, client):
        """Test para delegar tarea sin query."""
        response = client.post('/api/v1/delegate', 
                             json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delegate_with_query(self, client):
        """Test para delegar tarea con query válido."""
        response = client.post('/api/v1/delegate', 
                             json={'query': 'Hola, ¿cómo estás?'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
    
    def test_list_agents(self, client):
        """Test para listar agentes."""
        response = client.get('/api/v1/agents')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'agents' in data
        assert len(data['agents']) > 0
    
    def test_agent_health(self, client):
        """Test para health check de agentes."""
        response = client.get('/api/v1/health/agents')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'agents' in data

class TestAPIErrorHandling:
    """Tests para el manejo de errores de la API."""
    
    def test_invalid_json(self, client):
        """Test para JSON inválido."""
        response = client.post('/api/v1/delegate', 
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_malformed_request(self, client):
        """Test para request malformado."""
        response = client.post('/api/v1/delegate', 
                             json={'invalid': 'data'})
        assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__]) 