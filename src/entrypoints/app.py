from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from domain.models.models import Currency
from domain.ports.search_repository_port import SearchRepositoryPort
from entrypoints.assembly import build_search_repository

from utils.currency_check import currency_dep

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
    moneda: Currency = Depends(currency_dep),
    repo: SearchRepositoryPort = Depends(repo_dep)
):
    moneda = Currency(moneda).value
    today = date.today()
    try:
        if checkin<today:
            raise BookingDateValidationException()
        if checkin>=checkout:
            raise InvalidDateRangeException()
        query = repo.search_hotels(ciudad,checkin,checkout,group,rooms, moneda)
        return query
    except InvalidDateRangeException:
        raise HTTPException(400, "the check-in date is later than the check-out date")
    except BookingDateValidationException:
        raise HTTPException(400, "the check-in date is lower than today")
    except Exception as e:
        raise HTTPException(
            503,
            f"El servicio está temporalmente fuera de servicio: {str(e)}"
        )

@app.get("/search/search_cities")
def search_cities(repo: SearchRepositoryPort = Depends(repo_dep)):
    try:
        return repo.search_cities()
    except Exception as e:
        raise HTTPException(
            503,
            f"El servicio está temporalmente fuera de servicio: {str(e)}"
        )

@app.get("/search/detail_room")
def room_detail(
    habitacionId: str,
    checkin: date,
    checkout: date,
    moneda: Currency = Depends(currency_dep),
    repo: SearchRepositoryPort = Depends(repo_dep)
):
    moneda = Currency(moneda).value
    try:
        query = repo.room_detail(habitacionId, checkin, checkout, moneda)
        return query
    except RoomNotFound:
        raise HTTPException(404, "El recurso habitación no existe.")
    except RoomNotHavefee:
        raise HTTPException(409, "La habitación no puede ser mostrada, no tiene tarifa")
    except Exception as e:
        raise HTTPException(
            503,
            f"El servicio está temporalmente fuera de servicio: {str(e)}"
        )

@app.get("/search/ping")
def healthcheck():
    return "pong"
