from pydantic import BaseModel

from enum import Enum

from datetime import datetime

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    COP = "COP"

class HabitacionesDisponibles(BaseModel):
    id: str
    hotelId: str
    nombre_hotel: str
    descuento: float
    subtotal_sin_descuento: float
    subtotal_con_descuento: float
    total: float
    moneda: str
    direccion: str
    capacidad_maxima: int
    distancia: str
    acceso: str
    estrellas: int
    puntuacion_resena: float
    cantidad_resenas: int
    tipo_habitacion: str
    tipo_cama: list[str]
    tamano_habitacion: str
    amenidades: list[str]
    imagenes: list[str]

class HabitacionDetalle(BaseModel):
    id: str
    hotelId: str
    nombre_hotel: str
    descuento: float
    subtotal_sin_descuento: float
    subtotal_con_descuento: float
    total: float
    moneda: str
    direccion: str
    capacidad_maxima: int
    distancia: str
    acceso: str
    estrellas: int
    tipo_habitacion: str
    tipo_cama: list[str]
    tamano_habitacion: str
    amenidades: list[str]
    imagenes: list[str]
    latitud: float
    longitud: float

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
    tipo_habitacion: str
    tipo_cama: list[str]
    tamano_habitacion: str
    amenidades: list[str]

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
    distancia: str
    acceso: str

class Tarifa(BaseModel):
    id: str | None = None
    HabitacionId: str
    precioBase: float
    moneda: str
    fechaInicio: datetime
    fechaFin: datetime
    descuento: float

class Resena(BaseModel):
    id: str | None = None
    viajeroId: str
    hotelId: str
    reservaId: str
    calificacion: int
    comentario: str
    fecha: datetime
    verificada: bool