import pytest

from fastapi.testclient import TestClient

from adapters.memory.search_repository_memory import InMemorySearchRepositoryAdapter
from entrypoints.app import app, repo_dep

@pytest.fixture
def client():
    """Test client por test. Crea una nueva instancia del repositorio para cada test."""
    test_repo = InMemorySearchRepositoryAdapter()

    # Override la dependencia para usar este repositorio
    def _override_repo():
        return test_repo
    
    app.dependency_overrides[repo_dep] = _override_repo

    c = TestClient(app)
    return c

def test_search_hotels_correct(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2026-10-01&checkout=2026-10-12&group=1&rooms=1")
    assert get.status_code == 200
    #Es un array
    data = get.json()
    assert isinstance(data, list)
    
    #Revisar estructura de respuesta
    for item in data:
        assert "id" in item
        assert "nombre_hotel" in item
        assert "precio" in item
        assert "direccion" in item
        assert "capacidad_maxima" in item
        assert "tipo_habitacion" in item

def test_search_hotel_ci_greater_co(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2026-11-01&checkout=2026-10-12&group=1&rooms=1")
    assert get.status_code == 400
    
    data = get.json()

    #Validar mensaje de error
    assert data["detail"] == "the check-in date is later than the check-out date"

def test_search_hotel_ci_lower_today(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2010-11-01&checkout=2010-10-12&group=1&rooms=1")
    assert get.status_code == 400

    data = get.json()

    #Validar mensaje de error
    assert data["detail"] == "the check-in date is lower than today"

def test_invalid_parametters_date(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=11-01-2025&checkout=2010-10-12&group=1&rooms=1")
    assert get.status_code == 422

def test_invalid_parametters_string(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2026-10-01&checkout=2026-10-12&group=f&rooms=1")
    assert get.status_code == 422

def test_healthcheck(client: client):
    get = client.get("/search/ping")
    assert get.status_code == 200

    data = get.json()

    #Validar respuesta
    assert data == "pong"

def test_search_cities(client: client):
    get = client.get("/search/search_cities")
    assert get.status_code == 200
    data = get.json()
    assert isinstance(data, list)