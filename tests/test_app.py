import json
import pytest
from app import app

@pytest.fixture
def client():
    """Configuration de test pour l'application Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test que la route principale renvoie le bon message."""
    response = client.get('/')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Bienvenue sur l\'API de test'
    assert 'endpoints' in data
    assert '/ping' in data['endpoints']

def test_ping_endpoint(client):
    """Test que l'endpoint /ping répond avec 'pong'."""
    response = client.get('/ping')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'message' in data
    assert data['message'] == 'pong'

def test_invalid_endpoint(client):
    """Test qu'une route invalide renvoie un statut 404."""
    response = client.get('/route_inexistante')
    assert response.status_code == 404
