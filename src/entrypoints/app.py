from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from domain.models.models import Reserva, Habitacion, Hotel, HabitacionesDisponibles
from domain.ports.search_repository_port import SearchRepositoryPort
from entrypoints.assembly import build_search_repository

from error import (
    InvalidDateRangeException,
    BookingDateValidationException,
    RoomNotFound,
    RoomNotHavefee
    )
from config import ALLOWED_ORIGINS

def repo_dep() -> SearchRepositoryPort:
    return build_search_repository()


app = FastAPI(title="Search Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/search/search_rooms")
def buscar_habitacion(
    ciudad: str,
    checkin: date,
    checkout: date,
    group: int,
    rooms: int,
    repo: SearchRepositoryPort = Depends(repo_dep)
):
    today = date.today()
    try:
        if checkin<today:
            raise BookingDateValidationException()
        if checkin>=checkout:
            raise InvalidDateRangeException()
        query = repo.search_hotels(ciudad,checkin,checkout,group,rooms)
        return query
    except InvalidDateRangeException:
        raise HTTPException(400, "the check-in date is later than the check-out date")
    except BookingDateValidationException:
        raise HTTPException(400, "the check-in date is lower than today")
    except Exception:
        raise HTTPException(
            503,
            "El servicio está temporalmente fuera de servicio."
        )

@app.get("/search/search_cities")
def search_cities(repo: SearchRepositoryPort = Depends(repo_dep)):
    try:
        return repo.search_cities()
    except Exception:
        raise HTTPException(
            503,
            "El servicio está temporalmente fuera de servicio."
        )

@app.get("/search/detail_room")
def room_detail(
    habitacionId: str,
    checkin: date,
    checkout: date,
    repo: SearchRepositoryPort = Depends(repo_dep)
):
    try:
        query = repo.room_detail(habitacionId, checkin, checkout)
        return query
    except RoomNotFound:
        raise HTTPException(404, "El recurso habitación no existe.")
    except RoomNotHavefee:
        raise HTTPException(409, "La habitación no puede ser mostrada, no tiene tarifa")
    except Exception:
        raise HTTPException(
            503,
            "El servicio está temporalmente fuera de servicio."
        )

@app.get("/search/ping")
def healthcheck():
    return "pong"
