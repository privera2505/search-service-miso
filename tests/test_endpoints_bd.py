import pytest

from datetime import datetime
from unittest.mock import MagicMock, patch

from adapters.postgres.repository_adapter import (
    InBdSearchRepositoryAdapter
)

from adapters.postgres.models.models import (
    Habitacion,
    Hotel,
    Resena
)

from domain.models.models import (
    HabitacionDetalle,
    HabitacionesDisponibles
)

from error import (
    RoomNotFound,
    RoomNotHavefee
)


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def mock_session():
    session = MagicMock()
    yield session


@pytest.fixture
def repo(mock_session):

    with patch(
        "adapters.postgres.repository_adapter.db1.get_session",
        return_value=mock_session
    ), patch(
        "adapters.postgres.repository_adapter.db1.get_engine"
    ):
        repo = InBdSearchRepositoryAdapter()
        yield repo


# =========================================================
# HELPERS
# =========================================================

@pytest.fixture
def room():
    return Habitacion(
        id="room-id",
        hotelId="hotel-id",
        tipo="Doble",
        categoria="Deluxe",
        capacidadMaxima=4,
        descripcion="Vista ciudad",
        imagenes=["img1.jpg"],
        tipo_habitacion="Suite",
        tipo_cama=["King"],
        tamano_habitacion="35m2",
        amenidades=["WiFi", "AC"]
    )


@pytest.fixture
def hotel():
    return Hotel(
        id="hotel-id",
        nombre="Hotel Premium",
        direccion="Calle 123",
        ciudad="Madrid",
        pais="Spain",
        latitud=40.4168,
        longitud=-3.7038,
        estrellas=5,
        pmsProveedor="Opera",
        activo=True,
        distancia="2km",
        acceso="Metro"
    )


@pytest.fixture
def review():
    review = MagicMock()

    review.hotelId = "hotel-id"
    review.cantidad = 10
    review.promedio = 4.5

    return review


# =========================================================
# TEST SEARCH HOTELS
# =========================================================

@patch(
    "adapters.postgres.repository_adapter.convert_price",
    return_value=100
)
@patch(
    "adapters.postgres.repository_adapter.get_prices",
    return_value=(90, 108)
)
@patch.object(
    InBdSearchRepositoryAdapter,
    "_obtener_tarifa",
    return_value=(100, "EUR", 0.1)
)
def test_search_hotels_success(
    mock_tarifa,
    mock_prices,
    mock_convert,
    repo,
    mock_session,
    room,
    hotel,
    review
):

    tarifa = MagicMock()

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.join.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.group_by.return_value = query_mock

    query_mock.all.side_effect = [
        [(room, hotel, tarifa)],
        [review]
    ]

    result = repo.search_hotels(
        ciudad="Madrid",
        checkin=datetime(2026, 1, 1),
        checkout=datetime(2026, 1, 5),
        group=2,
        no_rooms=1,
        currency="USD"
    )

    assert len(result) == 1

    hotel_result = result[0]

    assert isinstance(hotel_result, HabitacionesDisponibles)

    assert hotel_result.id == room.id
    assert hotel_result.hotelId == hotel.id
    assert hotel_result.nombre_hotel == hotel.nombre
    assert hotel_result.total == 108


@patch.object(
    InBdSearchRepositoryAdapter,
    "_obtener_tarifa",
    return_value=(100, "EUR", 0.1)
)
def test_search_hotels_empty(
    mock_tarifa,
    repo,
    mock_session
):

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.join.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.group_by.return_value = query_mock

    query_mock.all.side_effect = [
        [],
        []
    ]

    result = repo.search_hotels(
        ciudad="Madrid",
        checkin=datetime(2026, 1, 1),
        checkout=datetime(2026, 1, 5),
        group=2,
        no_rooms=1,
        currency="USD"
    )

    assert result == []


@patch(
    "adapters.postgres.repository_adapter.convert_price",
    return_value=200
)
@patch(
    "adapters.postgres.repository_adapter.get_prices",
    return_value=(180, 216)
)
@patch.object(
    InBdSearchRepositoryAdapter,
    "_obtener_tarifa",
    return_value=(100, "EUR", 0.1)
)
def test_search_hotels_without_reviews(
    mock_tarifa,
    mock_prices,
    mock_convert,
    repo,
    mock_session,
    room,
    hotel
):

    tarifa = MagicMock()

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.join.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.group_by.return_value = query_mock

    query_mock.all.side_effect = [
        [(room, hotel, tarifa)],
        []
    ]

    result = repo.search_hotels(
        ciudad="Madrid",
        checkin=datetime(2026, 1, 1),
        checkout=datetime(2026, 1, 5),
        group=2,
        no_rooms=1,
        currency="USD"
    )

    assert len(result) == 1

    assert result[0].puntuacion_resena == 0
    assert result[0].cantidad_resenas == 0


# =========================================================
# TEST SEARCH CITIES
# =========================================================

def test_search_cities_success(
    repo,
    mock_session
):

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.filter.return_value = query_mock
    query_mock.distinct.return_value = query_mock

    query_mock.all.return_value = [
        ("Madrid",),
        ("Bogotá",),
        ("Cali",)
    ]

    result = repo.search_cities()

    assert result == [
        "Madrid",
        "Bogotá",
        "Cali"
    ]


def test_search_cities_empty(
    repo,
    mock_session
):

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.filter.return_value = query_mock
    query_mock.distinct.return_value = query_mock

    query_mock.all.return_value = []

    result = repo.search_cities()

    assert result == []


# =========================================================
# TEST ROOM DETAIL
# =========================================================

@patch(
    "adapters.postgres.repository_adapter.convert_price",
    return_value=100
)
@patch(
    "adapters.postgres.repository_adapter.get_prices",
    return_value=(90, 108)
)
@patch.object(
    InBdSearchRepositoryAdapter,
    "_obtener_tarifa",
    return_value=(100, "EUR", 0.1)
)
def test_room_detail_success(
    mock_tarifa,
    mock_prices,
    mock_convert,
    repo,
    mock_session,
    room,
    hotel
):

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.filter.return_value.first.side_effect = [
        room,
        hotel
    ]

    result = repo.room_detail(
        id_habitacion=room.id,
        checkin=datetime(2026, 1, 1),
        checkout=datetime(2026, 1, 5),
        currency="USD"
    )

    assert isinstance(result, HabitacionDetalle)

    assert result.id == room.id
    assert result.hotelId == hotel.id
    assert result.nombre_hotel == hotel.nombre
    assert result.total == 108


def test_room_detail_not_found(
    repo,
    mock_session
):

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.filter.return_value.first.return_value = None

    with pytest.raises(RoomNotFound):
        repo.room_detail(
            id_habitacion="invalid-room",
            checkin=datetime(2026, 1, 1),
            checkout=datetime(2026, 1, 5),
            currency="USD"
        )


@patch.object(
    InBdSearchRepositoryAdapter,
    "_obtener_tarifa",
    side_effect=RoomNotHavefee()
)
def test_room_detail_without_fee(
    mock_tarifa,
    repo,
    mock_session,
    room
):

    query_mock = MagicMock()

    mock_session.query.return_value = query_mock

    query_mock.filter.return_value.first.return_value = room

    with pytest.raises(RoomNotHavefee):
        repo.room_detail(
            id_habitacion=room.id,
            checkin=datetime(2026, 1, 1),
            checkout=datetime(2026, 1, 5),
            currency="USD"
        )


# =========================================================
# TEST OBTENER TARIFA
# =========================================================

@patch(
    "adapters.postgres.repository_adapter.TarifaClient"
)
def test_obtener_tarifa_success(
    mock_tarifa_client,
    repo
):

    tarifa_instance = MagicMock()

    tarifa_instance.obtener_tarifa_vigente.return_value = {
        "precioBase": 100,
        "moneda": "EUR",
        "descuento": 0.2
    }

    mock_tarifa_client.return_value = tarifa_instance

    precio, moneda, descuento = repo._obtener_tarifa(
        "room-id",
        datetime(2026, 1, 1)
    )

    assert precio == 100
    assert moneda == "EUR"
    assert descuento == 0.2


@patch(
    "adapters.postgres.repository_adapter.TarifaClient"
)
def test_obtener_tarifa_not_found(
    mock_tarifa_client,
    repo
):

    tarifa_instance = MagicMock()

    tarifa_instance.obtener_tarifa_vigente.return_value = None

    mock_tarifa_client.return_value = tarifa_instance

    with pytest.raises(RoomNotHavefee):
        repo._obtener_tarifa(
            "room-id",
            datetime(2026, 1, 1)
        )