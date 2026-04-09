# Implementaciones
from adapters.memory.search_repository_memory import InMemorySearchRepositoryAdapter
from adapters.postgres.repository_adapter import InBdSearchRepositoryAdapter
from domain.ports.search_repository_port import SearchRepositoryPort
from config import REPOSITORY_IMPL


def build_search_repository() -> SearchRepositoryPort:
    if REPOSITORY_IMPL == "postgres":
        InBdSearchRepositoryAdapter()
    return InMemorySearchRepositoryAdapter()