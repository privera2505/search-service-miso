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
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2026-10-01&checkout=2026-10-12&group=1&rooms=1&moneda=usd")
    assert get.status_code == 200
    #Es un array
    data = get.json()
    assert isinstance(data, list)
    
    #Revisar estructura de respuesta
    for item in data:
        assert "id" in item
        assert "nombre_hotel" in item
        assert "total" in item
        assert "direccion" in item
        assert "capacidad_maxima" in item
        assert "tipo_habitacion" in item

def test_search_hotel_ci_greater_co(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2026-11-01&checkout=2026-10-12&group=1&rooms=1&moneda=usd")
    assert get.status_code == 400
    
    data = get.json()

    #Validar mensaje de error
    assert data["detail"] == "the check-in date is later than the check-out date"

def test_search_hotel_ci_lower_today(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2010-11-01&checkout=2010-10-12&group=1&rooms=1&moneda=usd")
    assert get.status_code == 400

    data = get.json()

    #Validar mensaje de error
    assert data["detail"] == "the check-in date is lower than today"

def test_search_hotels_invalid_parametters_date(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=11-01-2025&checkout=2010-10-12&group=1&rooms=1&moneda=usd")
    assert get.status_code == 422

def test_search_hotels_invalid_currency(client: client):
    get = client.get("/search/search_rooms?ciudad=Madrid&checkin=2026-10-01&checkout=2026-10-12&group=f&rooms=1&moneda=hola")
    assert get.status_code == 422

def test_search_hotels_invalid_parametters_string(client: client):
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

def test_room_detail_correct(client: client):
    get = client.get(
        "/search/detail_room?habitacionId=22222222-2222-2222-2222-000000000001&checkin=2027-10-01&checkout=2027-10-03&moneda=usd"
    )

    assert get.status_code == 200

    # Es un objeto
    data = get.json()
    assert isinstance(data, dict)

    # Revisar estructura de respuesta
    assert "id" in data
    assert "nombre_hotel" in data
    assert "total" in data
    assert "moneda" in data
    assert "direccion" in data
    assert "capacidad_maxima" in data
    assert "distancia" in data
    assert "acceso" in data
    assert "estrellas" in data
    assert "tipo_habitacion" in data
    assert "tipo_cama" in data
    assert "tamano_habitacion" in data
    assert "amenidades" in data
    assert "imagenes" in data
    assert "latitud" in data
    assert "longitud" in data

def test_room_detail_no_room(client: client):
    get = client.get(
        "/search/detail_room?habitacionId=123&checkin=2026-10-01&checkout=2026-10-12&moneda=usd"
    )

    assert get.status_code == 404

def test_room_detail_no_fee(client:client):
    get = client.get(
        "/search/detail_room?habitacionId=22222222-2222-2222-2222-000000000001&checkin=2030-10-01&checkout=2030-10-12&moneda=usd"
    )

    assert get.status_code == 409

def test_room_detail_invalid_currency(client:client):
    get = client.get(
        "/search/detail_room?habitacionId=22222222-2222-2222-2222-000000000001&checkin=2030-10-01&checkout=2030-10-12&moneda=hola"
    )

    assert get.status_code == 422