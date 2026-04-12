from datetime import date, datetime
from math import ceil
from typing import Dict

from domain.models.models import Reserva, Habitacion, Hotel, HabitacionesDisponibles, Tarifa, Resena
from domain.ports.search_repository_port import SearchRepositoryPort


class InMemorySearchRepositoryAdapter(SearchRepositoryPort):
    def __init__(self) -> None:
        self._hotel: Dict[str, Hotel] = {
            "11111111-1111-1111-1111-000000000011": {
                "id": "11111111-1111-1111-1111-000000000011",
                "nombre": "Hotel del canto",
                "direccion": "Calle 123",
                "ciudad": "Madrid",
                "pais": "Spain",
                "latitud": 50.0755,
                "longitud": 14.4378,
                "estrellas": 5,
                "pmsProveedor": "Opera",
                "activo": True,
                "distancia": "3 km del centro",
                "acceso": "Metro"
            },
            "11111111-1111-1111-1111-000000000002": {
                "id": "11111111-1111-1111-1111-000000000002",
                "nombre": "Hotel del pesao",
                "direccion": "Gran Via 45",
                "ciudad": "Madrid",
                "pais": "Spain",
                "latitud": 40.4168,
                "longitud": -3.7038,
                "estrellas": 4,
                "pmsProveedor": "Fidelio",
                "activo": True,
                "distancia": "3 km del centro",
                "acceso": "Metro"
            }
        }

        self._habitacion: Dict[str, Habitacion] = {
            "22222222-2222-2222-2222-000000000001": {
                "id": "22222222-2222-2222-2222-000000000001",
                "hotelId": "11111111-1111-1111-1111-000000000011",
                "tipo": "Doble",
                "categoria": "Deluxe",
                "capacidadMaxima": 2,
                "descripcion": "Vista ciudad",
                "imagenes": ["img1.jpg"],
                "tipo_habitacion": "Deluxe",
                "tipo_cama": ["king"],
                "tamano_habitacion": "35m2",
                "amenidades": ["AC", "IDK"]
            },
            "22222222-2222-2222-2222-000000000002": {
                "id": "22222222-2222-2222-2222-000000000002",
                "hotelId": "11111111-1111-1111-1111-000000000011",
                "tipo": "Doble",
                "categoria": "Deluxe",
                "capacidadMaxima": 2,
                "descripcion": "Vista ciudad",
                "imagenes": ["img1.jpg"],
                "tipo_habitacion": "Deluxe",
                "tipo_cama": ["king"],
                "tamano_habitacion": "35m2",
                "amenidades": ["AC", "IDK"]
            },
            "22222222-2222-2222-2222-000000000003": {
                "id": "22222222-2222-2222-2222-000000000003",
                "hotelId": "11111111-1111-1111-1111-000000000002",
                "tipo": "Doble",
                "categoria": "Deluxe",
                "capacidadMaxima": 2,
                "descripcion": "Vista ciudad",
                "imagenes": ["img1.jpg"],
                "tipo_habitacion": "Deluxe",
                "tipo_cama": ["king"],
                "tamano_habitacion": "35m2",
                "amenidades": ["AC", "IDK"]
            },
            "22222222-2222-2222-2222-000000000004": {
                "id": "22222222-2222-2222-2222-000000000004",
                "hotelId": "11111111-1111-1111-1111-000000000002",
                "tipo": "Doble",
                "categoria": "Deluxe",
                "capacidadMaxima": 3,
                "descripcion": "Vista ciudad",
                "imagenes": ["img1.jpg"],
                "tipo_habitacion": "Deluxe",
                "tipo_cama": ["king"],
                "tamano_habitacion": "35m2",
                "amenidades": ["AC", "IDK"]
            }
        }

        self._reserva: Dict[str, Reserva] = {
            "33333333-3333-3333-3333-000000000001": {
                "id": "33333333-3333-3333-3333-000000000001",
                "codigo": "CODE1",
                "viajeroId": "44444444-4444-4444-4444-000000000001",
                "habitacionId": "22222222-2222-2222-2222-000000000001",
                "fechaCheckIn": datetime(2026, 9, 1, 15, 0),
                "fechaCheckOut": datetime(2026, 9, 3, 10, 0),
                "numHuespedes": 2,
                "estado": "CONFIRMADA",
                "subtotal": 200.0,
                "impuestos": 40.0,
                "total": 240.0,
                "moneda": "EUR"
            },
            "33333333-3333-3333-3333-000000000002": {
                "id": "33333333-3333-3333-3333-000000000002",
                "codigo": "CODE1",
                "viajeroId": "44444444-4444-4444-4444-000000000002",
                "habitacionId": "22222222-2222-2222-2222-000000000003",
                "fechaCheckIn": datetime(2026, 8, 1, 15, 0),
                "fechaCheckOut": datetime(2026, 8, 3, 10, 0),
                "numHuespedes": 2,
                "estado": "CONFIRMADA",
                "subtotal": 200.0,
                "impuestos": 40.0,
                "total": 240.0,
                "moneda": "EUR"
            }
        }

        self._tarifa: Dict[str, Tarifa] = {
            "55555555-5555-5555-5555-000000000001": {
                "id": "55555555-5555-5555-5555-000000000001",
                "HabitacionId": "22222222-2222-2222-2222-000000000001",
                "precioBase": 100.0,
                "moneda": "EUR",
                "fechaInicio": datetime(2024, 4, 1),
                "fechaFin": datetime(2028, 4, 30),
                "descuento": 0.1
            },
            "55555555-5555-5555-5555-000000000002": {
                "id": "55555555-5555-5555-5555-000000000002",
                "HabitacionId": "22222222-2222-2222-2222-000000000002",
                "precioBase": 150.0,
                "moneda": "EUR",
                "fechaInicio": datetime(2024, 4, 1),
                "fechaFin": datetime(2028, 4, 30),
                "descuento": 0.0
            },
            "55555555-5555-5555-5555-000000000003": {
                "id": "55555555-5555-5555-5555-000000000003",
                "HabitacionId": "22222222-2222-2222-2222-000000000003",
                "precioBase": 80.0,
                "moneda": "EUR",
                "fechaInicio": datetime(2024, 4, 1),
                "fechaFin": datetime(2028, 4, 30),
                "descuento": 0.0
            },
            "55555555-5555-5555-5555-000000000004": {
                "id": "55555555-5555-5555-5555-000000000004",
                "HabitacionId": "22222222-2222-2222-2222-000000000004",
                "precioBase": 400.0,
                "moneda": "EUR",
                "fechaInicio": datetime(2024, 4, 1),
                "fechaFin": datetime(2028, 4, 30),
                "descuento": 0.2
            }
        }

        self._resenas: Dict[str, Resena] = {
            "66666666-6666-6666-6666-000000000001": {
                "id": "66666666-6666-6666-6666-000000000001",
                "viajeroId": "77777777-7777-7777-7777-000000000001",
                "hotelId": "11111111-1111-1111-1111-000000000011",
                "reservaId": "33333333-3333-3333-3333-000000000001",
                "calificacion": 4,
                "comentario": "Buena",
                "fecha": datetime(2024, 4, 1),
                "verificacion": True
            },
            "66666666-6666-6666-6666-000000000002": {
                "id": "66666666-6666-6666-6666-000000000002",
                "viajeroId": "77777777-7777-7777-7777-000000000001",
                "hotelId": "11111111-1111-1111-1111-000000000011",
                "reservaId": "33333333-3333-3333-3333-000000000001",
                "calificacion": 3,
                "comentario": "Buena",
                "fecha": datetime(2024, 4, 1),
                "verificacion": True
            }
        }


    def search_hotels(self, ciudad: str, checkin: date, checkout: date, group: int, no_rooms: int) -> list[HabitacionesDisponibles]:
        # 1. Filtrar hoteles por ciudad
        hotels_by_city = [
            hotel
            for hotel in self._hotel.values()
            if hotel["ciudad"].lower() == ciudad.lower()
        ]

        hotel_ids = {hotel["id"] for hotel in hotels_by_city}

        # 2. Filtrar habitaciones por capacidad
        personas_por_habitacion = ceil(group/no_rooms)

        habitaciones = [
            habitacion
            for habitacion in self._habitacion.values()
            if habitacion["hotelId"] in hotel_ids
            and habitacion["capacidadMaxima"] >= personas_por_habitacion
        ]

        habitaciones_disponibles: list[HabitacionesDisponibles] = []

        # 3. Validar disponibilidad + calcular precio
        for habitacion in habitaciones:

            ocupada = any(
                reserva["habitacionId"] == habitacion["id"] and not (
                    checkout <= reserva["fechaCheckIn"].date()
                    or checkin >= reserva["fechaCheckOut"].date()
                )
                for reserva in self._reserva.values()
            )

            if ocupada:
                continue

            precio, moneda = self._calculate_price(
                habitacion["id"], checkin, checkout
            )

            if precio == 0:
                continue

            hotel = self._hotel[habitacion["hotelId"]]

            total_resenas, promedio_resenas = self._get_reviews_stats(habitacion["hotelId"])

            habitaciones_disponibles.append(
                HabitacionesDisponibles(
                    id=habitacion["id"],
                    nombre_hotel=hotel["nombre"],
                    precio=precio,
                    moneda= moneda,
                    direccion=hotel["direccion"],
                    capacidad_maxima=habitacion["capacidadMaxima"],
                    distancia=hotel["distancia"],
                    acceso=hotel["acceso"],
                    estrellas=hotel["estrellas"],
                    cantidad_resenas= total_resenas,
                    puntuacion_resena= promedio_resenas,
                    tipo_habitacion=habitacion["tipo_habitacion"],
                    tipo_cama=habitacion["tipo_cama"],
                    tamano_habitacion=habitacion["tamano_habitacion"],
                    amenidades=habitacion["amenidades"],
                    imagenes=habitacion["imagenes"]
                )
            )

        # 4. Agrupar por hotel y validar número de habitaciones
        resultado_final: list[HabitacionesDisponibles] = []

        habitaciones_por_hotel: Dict[str, list] = {}

        for hab in habitaciones_disponibles:
            habitaciones_por_hotel.setdefault(hab.nombre_hotel, []).append(hab)

        for hotel, habs in habitaciones_por_hotel.items():
            if len(habs) >= no_rooms:
                resultado_final.extend(habs)

        return resultado_final
    
    def _calculate_price(self, habitacion_id: str, checkin: date, checkout: date) -> float:
        noches = (checkout - checkin).days

        tarifas_validas = [
            tarifa
            for tarifa in self._tarifa.values()
            if tarifa["HabitacionId"] == habitacion_id
            and tarifa["fechaInicio"].date() <= checkin
            and tarifa["fechaFin"].date() >= checkout
        ]

        if not tarifas_validas:
            return 0.0

        tarifa = tarifas_validas[0]

        precio_base = tarifa["precioBase"]
        descuento = tarifa["descuento"]

        precio_final = precio_base * noches * (1 - descuento)

        return precio_final, tarifa["moneda"]
    
    def _get_reviews_stats(self, hotel_id: str) -> tuple[int, float]:
        resenas = [
            r for r in self._resenas.values()
            if r["hotelId"] == hotel_id
        ]

        if not resenas:
            return 0, 0.0

        total = len(resenas)
        promedio = sum(r["calificacion"] for r in resenas) / total

        return total, round(promedio, 1)
    
    def search_cities(self) -> list[str]:
        ciudades = {hotel["ciudad"] for hotel in self._hotel.values()}
        return list(ciudades)