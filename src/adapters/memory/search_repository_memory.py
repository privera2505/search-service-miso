from datetime import date, datetime
from typing import Dict

from domain.models.models import Reserva, Habitacion, Hotel, HabitacionesDisponibles
from domain.ports.search_repository_port import SearchRepositoryPort


class InMemorySearchRepositoryAdapter(SearchRepositoryPort):
    def __init__(self) -> None:
        self._hotel: Dict[str, Hotel] = {
            "11111111-1111-1111-1111-000000000001": {
                "id": "11111111-1111-1111-1111-000000000001",
                "nombre": "Grand Prague Hotel",
                "direccion": "Calle 123",
                "ciudad": "Prague",
                "pais": "Czech Republic",
                "latitud": 50.0755,
                "longitud": 14.4378,
                "estrellas": 5,
                "pmsProveedor": "Opera",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000002": {
                "id": "11111111-1111-1111-1111-000000000002",
                "nombre": "Madrid Central Hotel",
                "direccion": "Gran Via 45",
                "ciudad": "Madrid",
                "pais": "Spain",
                "latitud": 40.4168,
                "longitud": -3.7038,
                "estrellas": 4,
                "pmsProveedor": "Fidelio",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000003": {
                "id": "11111111-1111-1111-1111-000000000003",
                "nombre": "Paris Boutique Stay",
                "direccion": "Rue Rivoli",
                "ciudad": "Paris",
                "pais": "France",
                "latitud": 48.8566,
                "longitud": 2.3522,
                "estrellas": 5,
                "pmsProveedor": "Opera",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000004": {
                "id": "11111111-1111-1111-1111-000000000004",
                "nombre": "Berlin Comfort Inn",
                "direccion": "Alexanderplatz",
                "ciudad": "Berlin",
                "pais": "Germany",
                "latitud": 52.52,
                "longitud": 13.405,
                "estrellas": 3,
                "pmsProveedor": "Cloudbeds",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000005": {
                "id": "11111111-1111-1111-1111-000000000005",
                "nombre": "Rome Luxury Suites",
                "direccion": "Via Veneto",
                "ciudad": "Rome",
                "pais": "Italy",
                "latitud": 41.9028,
                "longitud": 12.4964,
                "estrellas": 5,
                "pmsProveedor": "Opera",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000006": {
                "id": "11111111-1111-1111-1111-000000000006",
                "nombre": "Lisbon Sea View",
                "direccion": "Av Atlantica",
                "ciudad": "Lisbon",
                "pais": "Portugal",
                "latitud": 38.7223,
                "longitud": -9.1393,
                "estrellas": 4,
                "pmsProveedor": "Fidelio",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000007": {
                "id": "11111111-1111-1111-1111-000000000007",
                "nombre": "Amsterdam Canal Hotel",
                "direccion": "Canal St",
                "ciudad": "Amsterdam",
                "pais": "Netherlands",
                "latitud": 52.3676,
                "longitud": 4.9041,
                "estrellas": 4,
                "pmsProveedor": "Cloudbeds",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000008": {
                "id": "11111111-1111-1111-1111-000000000008",
                "nombre": "Vienna Imperial",
                "direccion": "Ringstrasse",
                "ciudad": "Vienna",
                "pais": "Austria",
                "latitud": 48.2082,
                "longitud": 16.3738,
                "estrellas": 5,
                "pmsProveedor": "Opera",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000009": {
                "id": "11111111-1111-1111-1111-000000000009",
                "nombre": "Barcelona Beach Hotel",
                "direccion": "La Rambla",
                "ciudad": "Barcelona",
                "pais": "Spain",
                "latitud": 41.3851,
                "longitud": 2.1734,
                "estrellas": 4,
                "pmsProveedor": "Fidelio",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000010": {
                "id": "11111111-1111-1111-1111-000000000010",
                "nombre": "London City Lodge",
                "direccion": "Baker Street",
                "ciudad": "London",
                "pais": "UK",
                "latitud": 51.5074,
                "longitud": -0.1278,
                "estrellas": 3,
                "pmsProveedor": "Cloudbeds",
                "activo": True
            },
            "11111111-1111-1111-1111-000000000011": {
                "id": "11111111-1111-1111-1111-000000000011",
                "nombre": "Bogota Business Hotel",
                "direccion": "Zona T",
                "ciudad": "Bogota",
                "pais": "Colombia",
                "latitud": 4.7110,
                "longitud": -74.0721,
                "estrellas": 4,
                "pmsProveedor": "Opera",
                "activo": True
            }
        }

        self._habitacion: Dict[str, Habitacion] = {
            "22222222-2222-2222-2222-000000000001": {
                "id": "22222222-2222-2222-2222-000000000001",
                "hotelId": "11111111-1111-1111-1111-000000000001",
                "tipo": "Doble",
                "categoria": "Deluxe",
                "capacidadMaxima": 2,
                "descripcion": "Vista ciudad",
                "imagenes": ["img1.jpg"]
            },
            "22222222-2222-2222-2222-000000000002": {
                "id": "22222222-2222-2222-2222-000000000002",
                "hotelId": "11111111-1111-1111-1111-000000000002",
                "tipo": "Suite",
                "categoria": "Premium",
                "capacidadMaxima": 3,
                "descripcion": "Suite céntrica",
                "imagenes": ["img2.jpg"]
            },
            "22222222-2222-2222-2222-000000000003": {
                "id": "22222222-2222-2222-2222-000000000003",
                "hotelId": "11111111-1111-1111-1111-000000000003",
                "tipo": "Doble",
                "categoria": "Deluxe",
                "capacidadMaxima": 2,
                "descripcion": "Vista torre",
                "imagenes": ["img3.jpg"]
            },
            "22222222-2222-2222-2222-000000000004": {
                "id": "22222222-2222-2222-2222-000000000004",
                "hotelId": "11111111-1111-1111-1111-000000000004",
                "tipo": "Simple",
                "categoria": "Standard",
                "capacidadMaxima": 1,
                "descripcion": "Económica",
                "imagenes": ["img4.jpg"]
            },
            "22222222-2222-2222-2222-000000000005": {
                "id": "22222222-2222-2222-2222-000000000005",
                "hotelId": "11111111-1111-1111-1111-000000000005",
                "tipo": "Suite",
                "categoria": "Luxury",
                "capacidadMaxima": 4,
                "descripcion": "Lujo total",
                "imagenes": ["img5.jpg"]
            },
            "22222222-2222-2222-2222-000000000006": {
                "id": "22222222-2222-2222-2222-000000000006",
                "hotelId": "11111111-1111-1111-1111-000000000006",
                "tipo": "Doble",
                "categoria": "Standard",
                "capacidadMaxima": 2,
                "descripcion": "Vista mar",
                "imagenes": ["img6.jpg"]
            },
            "22222222-2222-2222-2222-000000000007": {
                "id": "22222222-2222-2222-2222-000000000007",
                "hotelId": "11111111-1111-1111-1111-000000000007",
                "tipo": "Doble",
                "categoria": "Standard",
                "capacidadMaxima": 2,
                "descripcion": "Canal view",
                "imagenes": ["img7.jpg"]
            },
            "22222222-2222-2222-2222-000000000008": {
                "id": "22222222-2222-2222-2222-000000000008",
                "hotelId": "11111111-1111-1111-1111-000000000008",
                "tipo": "Suite",
                "categoria": "Luxury",
                "capacidadMaxima": 3,
                "descripcion": "Imperial",
                "imagenes": ["img8.jpg"]
            },
            "22222222-2222-2222-2222-000000000009": {
                "id": "22222222-2222-2222-2222-000000000009",
                "hotelId": "11111111-1111-1111-1111-000000000009",
                "tipo": "Doble",
                "categoria": "Standard",
                "capacidadMaxima": 2,
                "descripcion": "Beach",
                "imagenes": ["img9.jpg"]
            },
            "22222222-2222-2222-2222-000000000010": {
                "id": "22222222-2222-2222-2222-000000000010",
                "hotelId": "11111111-1111-1111-1111-000000000010",
                "tipo": "Simple",
                "categoria": "Standard",
                "capacidadMaxima": 1,
                "descripcion": "City basic",
                "imagenes": ["img10.jpg"]
            },
            "22222222-2222-2222-2222-000000000011": {
                "id": "22222222-2222-2222-2222-000000000011",
                "hotelId": "11111111-1111-1111-1111-000000000011",
                "tipo": "Doble",
                "categoria": "Business",
                "capacidadMaxima": 2,
                "descripcion": "Business",
                "imagenes": ["img11.jpg"]
            }
        }

        self._reserva: Dict[str, Reserva] = {
            "33333333-3333-3333-3333-000000000001": {
                "id": "33333333-3333-3333-3333-000000000001",
                "codigo": "CODE1",
                "viajeroId": "44444444-4444-4444-4444-000000000001",
                "habitacionId": "22222222-2222-2222-2222-000000000001",
                "fechaCheckIn": datetime(2026, 4, 1, 15, 0),
                "fechaCheckOut": datetime(2026, 4, 3, 11, 0),
                "numHuespedes": 2,
                "estado": "CONFIRMADA",
                "subtotal": 200.0,
                "impuestos": 40.0,
                "total": 240.0,
                "moneda": "EUR"
            },
            "33333333-3333-3333-3333-000000000002": {
                "id": "33333333-3333-3333-3333-000000000002",
                "codigo": "CODE2",
                "viajeroId": "44444444-4444-4444-4444-000000000002",
                "habitacionId": "22222222-2222-2222-2222-000000000002",
                "fechaCheckIn": datetime(2026, 4, 2, 15, 0),
                "fechaCheckOut": datetime(2026, 4, 5, 11, 0),
                "numHuespedes": 3,
                "estado": "CONFIRMADA",
                "subtotal": 250.0,
                "impuestos": 50.0,
                "total": 300.0,
                "moneda": "EUR"
            },
            "33333333-3333-3333-3333-000000000003": {
                "id": "33333333-3333-3333-3333-000000000003",
                "codigo": "CODE3",
                "viajeroId": "44444444-4444-4444-4444-000000000003",
                "habitacionId": "22222222-2222-2222-2222-000000000003",
                "fechaCheckIn": datetime(2026, 4, 3, 15, 0),
                "fechaCheckOut": datetime(2026, 4, 6, 11, 0),
                "numHuespedes": 2,
                "estado": "CONFIRMADA",
                "subtotal": 260.0,
                "impuestos": 52.0,
                "total": 312.0,
                "moneda": "EUR"
            }
        }

    def search_hotels(self, ciudad: str, checkin: date, checkout: date, group: int, no_rooms: int) -> list[HabitacionesDisponibles]:
        #Filtrar hoteles por ciudad
        hotels_by_city = [
            hotel
            for hotel in self._hotel.values()
            if hotel["ciudad"].lower() == ciudad.lower()
        ]

        #Filtrar habitaciones por los hoteles obtenidos y si la habitacion al menos puede hospedar a la cantidad de personas.
        hotel_ids = {hotel["id"] for hotel in hotels_by_city}

        habitaciones = [
            habitacion
            for habitacion in self._habitacion.values()
            if habitacion["hotelId"] in hotel_ids
            and habitacion["capacidadMaxima"] >= group
        ]

        habitaciones_disponibles: list[HabitacionesDisponibles] = []

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

            hotel = self._hotel[habitacion["hotelId"]]

            habitaciones_disponibles.append(
                HabitacionesDisponibles(
                    id=habitacion["id"],
                    nombre_hotel=hotel["nombre"],
                    precio=10,
                    direccion=hotel["direccion"],
                    capacidad_maxima=habitacion["capacidadMaxima"]
                )
            )
        return habitaciones_disponibles