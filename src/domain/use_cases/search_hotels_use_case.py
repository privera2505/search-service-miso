from domain.ports.search_repository_port import SearchRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from domain.models.models import HabitacionesDisponibles

from datetime import date

class SearchHotelsUseCase(BaseUseCase):
    """Use case for search hotels"""

    def __init__(self, search_repository: SearchRepositoryPort):
        self.search_repository = search_repository
    
    def execute(self, ciudad: str, checkin: date, checkout: date, group: int, no_rooms: int) -> list[HabitacionesDisponibles]:
        return self.search_repository.search_hotels(ciudad, checkin, checkout, group, no_rooms)
