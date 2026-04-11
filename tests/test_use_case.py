from typing import List
from datetime import date

from adapters.memory.search_repository_memory import InMemorySearchRepositoryAdapter
from domain.models.models import HabitacionesDisponibles
from domain.use_cases.search_cities_use_case import SearchCitiesUseCase
from domain.use_cases.search_hotels_use_case import SearchHotelsUseCase

def test_search_hotels_use_case():
    repo = InMemorySearchRepositoryAdapter()
    uc = SearchHotelsUseCase(repo)

    ciudad = "Madrid"
    checkin = date(2026, 10, 1)
    checkout = date(2026, 10, 12)
    group = 1
    no_rooms = 1

    query = uc.execute(
        ciudad=ciudad,
        checkin=checkin,
        checkout=checkout,
        group=group,
        no_rooms=no_rooms
    )

    assert query is not None
    assert isinstance(query, list)

    # opcional: validar contenido
    if query:
        first = query[0]
        assert hasattr(first, "id")
        assert hasattr(first, "nombre_hotel")
    
def test_search_cities_use_case():
    repo = InMemorySearchRepositoryAdapter()
    uc = SearchCitiesUseCase(repo)

    query = uc.execute()

    assert query is not None
    assert isinstance(query, list)

    #validar que todos sean strings
    assert all(isinstance(city, str) for city in query)