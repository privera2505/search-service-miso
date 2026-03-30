from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import date

from domain.models.models import Reserva, Habitacion, Hotel, HabitacionesDisponibles
from domain.ports.search_repository_port import SearchRepositoryPort
from entrypoints.assembly import build_search_repository

from error import (
    InvalidDateRangeException
    )


repo_instance = build_search_repository()


def repo_dep() -> SearchRepositoryPort:
    return repo_instance


app = FastAPI(title="Search Service API")

@app.get("/api/search_rooms")
def buscar_habitacion(
    ciudad: str,
    checkin: date,
    checkout: date,
    group: int,
    rooms: int
):
    try:
        if checkin>=checkout:
            raise InvalidDateRangeException()
        print(ciudad)
        print(checkin)
        print(checkout)
        print(group)
        print(rooms)
    except InvalidDateRangeException:
        raise HTTPException(400, "the check-in date is later than the check-out date")