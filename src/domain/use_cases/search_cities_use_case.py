from domain.ports.search_repository_port import SearchRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase

from datetime import date

class SearchCitiesUseCase(BaseUseCase):
    """Use case for search hotels"""

    def __init__(self, search_repository: SearchRepositoryPort):
        self.search_repository = search_repository
    
    def execute(self) -> list[str]:
        return self.search_repository.search_cities()
