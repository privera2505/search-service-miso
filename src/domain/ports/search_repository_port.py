from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from domain.models.models import HabitacionesDisponibles , HabitacionDetalle


class SearchRepositoryPort(ABC):
    """Posts repository interface."""

    # Done.
    @abstractmethod
    def search_hotels(self, ciudad: str, checkin: date, checkout: date, group: int, no_rooms: int, moneda: str) -> List[HabitacionesDisponibles]:
        """Returns a list of available hotels with city, checkin, checkout, group and no_romms filter."""
        pass

    @abstractmethod
    def search_cities(self) -> list[str]:
        """Returns a list of available cities where you can book a hotel"""
        pass

    @abstractmethod
    def room_detail(self, id_habitacion: str, checkin: date, checkout: date, moneda: str) -> HabitacionDetalle:
        """Return the detail of a room."""
        pass