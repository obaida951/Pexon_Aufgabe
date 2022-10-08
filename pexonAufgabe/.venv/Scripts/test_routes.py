# mit "pytest test_routes" kann diese Test durchgeführt werden 
import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_home_bad_http_method(client):
    resp = client.post('/')
    assert resp.status_code == 405

def test_create_http_method(client):
    resp = client.get('/create/')
    assert resp.status_code == 200

    

    