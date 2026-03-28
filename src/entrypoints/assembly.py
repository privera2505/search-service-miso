# Implementaciones
from adapters.memory.search_repository_memory import InMemorySearchRepositoryAdapter
from domain.ports.search_repository_port import SearchRepositoryPort
from main import REPOSITORY_IMPL


def build_search_repository() -> SearchRepositoryPort:
    if REPOSITORY_IMPL == "postgres":
        pass
    return InMemorySearchRepositoryAdapter()