from pydantic import BaseModel

from datetime import datetime


class HabitacionesDisponibles(BaseModel):
    id: str
    nombre_hotel: str
    precio: float
    direccion: str
    capacidad_maxima: int


class Reserva(BaseModel):
    id: str | None = None
    codigo: str
    viajeroId: str
    habitacionId: str
    fechaCheckIn: datetime
    fechaCheckOut: datetime
    numHuespedes: int
    estado: str
    subtotal: float
    impuestos: float
    total: float
    moneda: str

class Habitacion(BaseModel):
    id: str | None = None
    hotelId: str
    tipo: str
    categoria: str
    capacidadMaxima: int
    descripcion: str
    imagenes: list[str]

class Hotel(BaseModel):
    id: str | None = None
    nombre: str
    direccion: str
    ciudad: str
    pais: str
    latitud: float
    longitud: float
    estrellas: int
    pmsProveedor: str
    activo: bool