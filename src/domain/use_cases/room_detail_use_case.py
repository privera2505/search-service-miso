from domain.ports.search_repository_port import SearchRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase

from datetime import date

from domain.models.models import HabitacionDetalle

class RoomDetailUseCase(BaseUseCase):
    """Use case for room detail"""

    def __init__(self, search_repository: SearchRepositoryPort):
        self.search_repository = search_repository
    
    def execute(self, id_habitacion: str, checkin: date, checkout: date, moneda: str) -> HabitacionDetalle:
        return self.search_repository.room_detail(id_habitacion, checkin, checkout, moneda)