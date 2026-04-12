from adapters.postgres.models.models import Base
from adapters.postgres.declarative_base import db1
from domain.ports.search_repository_port import SearchRepositoryPort
from domain.models.models import HabitacionesDisponibles

from sqlalchemy import func, select, exists

from math import ceil

from adapters.postgres.models.models import Reserva, Hotel, Habitacion, Tarifa, Resena


class InBdSearchRepositoryAdapter(SearchRepositoryPort):
    "In BD Implementation of SearchRepository"

    def __init__(self):
        Base.metadata.create_all(db1.get_engine())
    
    def search_hotels(self, ciudad, checkin, checkout, group, no_rooms) -> list[HabitacionesDisponibles]:
        db = db1.get_session()
        personas_por_habitacion = ceil(group/no_rooms)
        try:
            #Query Principal
            results = (
                db.query(Habitacion, Hotel, Tarifa)
                .join(Hotel, Habitacion.hotelId == Hotel.id)
                .join(Tarifa, Tarifa.habitacionId == Habitacion.id)
                .filter(
                    Hotel.ciudad == ciudad,
                    Hotel.activo == True,
                    Habitacion.capacidadMaxima >= personas_por_habitacion,
                    Tarifa.fechaInicio <= checkin,
                    Tarifa.fechaFin >= checkout,
                    ~exists().where(
                        Reserva.habitacionId == Habitacion.id,
                        Reserva.fechaCheckIn < checkout,
                        Reserva.fechaCheckOut > checkin
                    )
                )
                .all()
            )

            #Obtener calificaciones por hotel
            hotels_ids = list({hotel.id for _, hotel, _ in results})

            review_data = (
                db.query(
                    Resena.hotelId,
                    func.count(Resena.id).label("cantidad"),
                    func.avg(Resena.calificacion).label("promedio")
                )
                .filter(Resena.hotelId.in_(hotels_ids))
                .group_by(Resena.hotelId)
                .all()
            )
            reviews_map = {
                r.hotelId: {
                    "Cantidad": r.cantidad,
                    "Promedio": float(r.promedio)
                }
                for r in review_data
            }

            #Transformar al modelo 
            disponibles: list[HabitacionesDisponibles] = [
                HabitacionesDisponibles(
                    id=habitacion.id,
                    nombre_hotel=hotel.nombre,
                    precio=tarifa.precioBase * (1 - tarifa.descuento),
                    moneda=tarifa.moneda,
                    direccion=hotel.direccion,
                    capacidad_maxima=habitacion.capacidadMaxima,
                    distancia=hotel.distancia,
                    acceso=hotel.acceso,
                    estrellas=hotel.estrellas,
                    puntuacion_resena=reviews_map.get(hotel.id, {}).get("promedio", 0),
                    cantidad_resenas=reviews_map.get(hotel.id, {}).get("cantidad", 0),
                    tipo_habitacion=habitacion.tipo_habitacion,
                    tipo_cama=habitacion.tipo_cama,
                    tamano_habitacion=habitacion.tamano_habitacion,
                    amenidades=habitacion.amenidades,
                    imagenes=habitacion.imagenes
                )
                for habitacion, hotel, tarifa in results
            ]

            return disponibles

        finally:
            db.close()
    
    def search_cities(self) -> list[str]:
        db = db1.get_session()
        try:
            ciudades = (
                db.query(Hotel.ciudad)
                .filter(Hotel.activo == True)
                .distinct()
                .all()
            )
            return [c[0] for c in ciudades]
        finally:
            db.close()
        return 