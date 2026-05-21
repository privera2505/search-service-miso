from adapters.postgres.models.models import Base
from adapters.postgres.declarative_base import db1
from domain.ports.search_repository_port import SearchRepositoryPort
from domain.models.models import HabitacionDetalle, HabitacionesDisponibles

from sqlalchemy import func, select, exists

from utils.currency_converter import convert_price
from utils.prices_calculator import get_prices
from utils.get_fare import TarifaClient

from math import ceil

from adapters.postgres.models.models import Reserva, Hotel, Habitacion, Tarifa, Resena, Disponibilidad
from error import RoomNotFound, RoomNotHavefee


class InBdSearchRepositoryAdapter(SearchRepositoryPort):
    "In BD Implementation of SearchRepository"

    def __init__(self):
        Base.metadata.create_all(db1.get_engine())
    
    def search_hotels(self, ciudad, checkin, checkout, group, no_rooms, currency) -> list[HabitacionesDisponibles]:
        db = db1.get_session()
        personas_por_habitacion = ceil(group/no_rooms)
        try:
            noches = (checkout - checkin).days
            # Obtener habitación valida del país/ciudad
            habitaciones_validas_subquery = (
                db.query(Habitacion.id.label("habitacionId"))
                .join(Hotel, Habitacion.hotelId == Hotel.id)
                .filter(
                    Hotel.ciudad == ciudad,
                    Hotel.activo == True,
                    Habitacion.capacidadMaxima >= personas_por_habitacion
                )
                .subquery()
            )

            # Validar disponibilidad
            disponibilidad_subquery = (
                db.query(
                    Disponibilidad.habitacionId
                )
                .filter(
                    Disponibilidad.habitacionId.in_(
                        db.query(habitaciones_validas_subquery.c.habitacionId)
                    ),
                    Disponibilidad.fecha >= checkin,
                    Disponibilidad.fecha < checkout,
                    Disponibilidad.unidadesDisponibles > 0
                )
                .group_by(Disponibilidad.habitacionId)
                .having(func.count(func.distinct(Disponibilidad.fecha)) == noches)
                .subquery()
            )
            
            #Query Principal
            results = (
                db.query(Habitacion, Hotel)
                .join(Hotel, Habitacion.hotelId == Hotel.id)
                .join(
                    disponibilidad_subquery,
                    disponibilidad_subquery.c.habitacionId == Habitacion.id
                )
                .all()
            )

            #Obtener calificaciones por hotel
            hotels_ids = list({hotel.id for _, hotel in results})

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

            disponibles: list[HabitacionesDisponibles] = []

            for habitacion, hotel in results:

                precioBase, moneda, descuento = self._obtener_tarifa(habitacion.id, checkin)

                subtotal_sin_descuento_curr_tarifa = precioBase * noches

                subtotal_sin_descuento_curr_query = convert_price(subtotal_sin_descuento_curr_tarifa, moneda, currency)

                subtotal_con_descuento_curr_query, total_curr_query = get_prices(subtotal_sin_descuento_curr_query, descuento, 0.20)

                disponibles.append(
                    HabitacionesDisponibles(
                        id=habitacion.id,
                        hotelId= hotel.id,
                        nombre_hotel=hotel.nombre,
                        descuento=descuento,
                        subtotal_sin_descuento=round(subtotal_sin_descuento_curr_query,2),
                        subtotal_con_descuento= round(subtotal_con_descuento_curr_query,2),
                        total=round(total_curr_query,2),
                        moneda=currency,
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
                )

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

    def room_detail(self, id_habitacion, checkin, checkout, currency):
        db = db1.get_session()
        noches = (checkout - checkin).days
        try:
            #Validar habitacion
            habitacion = (
                db.query(Habitacion)
                .filter(Habitacion.id == id_habitacion)
                .first()
            )
            if habitacion is None:
                raise RoomNotFound
            
            #Buscar tarifa vigente

            precioBase, moneda, descuento = self._obtener_tarifa(id_habitacion, checkin)
            
            #Buscar el hotel
            hotel = (
                db.query(Hotel)
                .filter(
                    Hotel.id == habitacion.hotelId,
                    Hotel.activo.is_(True)
                )
                .first()
            )

            subtotal_sin_descuento_curr_tarifa = precioBase * noches

            subtotal_sin_descuento_curr_query = convert_price(subtotal_sin_descuento_curr_tarifa, moneda, currency)

            subtotal_con_descuento_curr_query, total_curr_query = get_prices(subtotal_sin_descuento_curr_query, descuento, 0.20)

            habitacion_detalle = HabitacionDetalle(
                id=habitacion.id,
                hotelId=hotel.id,
                nombre_hotel=hotel.nombre,
                descuento=descuento,
                subtotal_sin_descuento=round(subtotal_sin_descuento_curr_query,2),
                subtotal_con_descuento= round(subtotal_con_descuento_curr_query,2),
                total=round(total_curr_query,2),
                moneda=currency,
                direccion=hotel.direccion,
                capacidad_maxima=habitacion.capacidadMaxima,
                distancia=hotel.distancia,
                acceso=hotel.acceso,
                estrellas=hotel.estrellas,
                tipo_habitacion=habitacion.tipo_habitacion,
                tipo_cama=habitacion.tipo_cama,
                tamano_habitacion=habitacion.tamano_habitacion,
                amenidades=habitacion.amenidades,
                imagenes=habitacion.imagenes,
                latitud=hotel.latitud,
                longitud=hotel.longitud
            )

            return habitacion_detalle

        finally:
            db.close()

    def _obtener_tarifa(self, id_habitacion, checkin):
        tarifa_client = TarifaClient()

        tarifa = tarifa_client.obtener_tarifa_vigente(
            id_habitacion,
            checkin
        )

        if tarifa is None:
            raise RoomNotHavefee()

        return tarifa["precioBase"], tarifa["moneda"], tarifa["descuento"]