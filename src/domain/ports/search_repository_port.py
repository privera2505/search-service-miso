from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from domain.models.models import HabitacionesDisponibles 


class SearchRepositoryPort(ABC):
    """Posts repository interface."""

    # Done.
    @abstractmethod
    def search_hotels(self, ciudad: str, checkin: date, checkout: date, group: int, no_rooms: int) -> List[HabitacionesDisponibles]:
        """Returns a list of available hotels with city, checkin, checkout, group and no_romms filter."""
        pass