from datetime import datetime

from adapters.postgres.models.models import Base, Hotel, Habitacion, Reserva, Tarifa, Resena
from adapters.postgres.declarative_base import db1  # 👈 donde tienes tu GetDB


def init_db():
    engine = db1.get_engine()

    #Crear tablas
    Base.metadata.create_all(bind=engine)

    session = db1.get_session()

    #Evitar duplicados
    if session.query(Hotel).first():
        print("DB ya inicializada")
        session.close()
        return

    # HOTELS
    hoteles = [
        Hotel(
            id="11111111-1111-1111-1111-000000000001",
            nombre="Hotel 1",
            direccion="Calle 123",
            ciudad="Madrid",
            pais="Spain",
            latitud=50.0755,
            longitud=14.4378,
            estrellas=5,
            pmsProveedor="Opera",
            activo=True,
            distancia="3 km del centro",
            acceso="Metro"
        ),
        Hotel(
            id="11111111-1111-1111-1111-000000000002",
            nombre="Hotel 2",
            direccion="Gran Via 45",
            ciudad="Madrid",
            pais="Spain",
            latitud=40.4168,
            longitud=-3.7038,
            estrellas=4,
            pmsProveedor="Fidelio",
            activo=True,
            distancia="3 km del centro",
            acceso="Metro"
        ),
    ]
    session.add_all(hoteles)
    session.commit()

    # HABITACIONES
    habitaciones = [
        Habitacion(
            id="22222222-2222-2222-2222-000000000001",
            hotelId="11111111-1111-1111-1111-000000000001",
            tipo="Doble",
            categoria="Deluxe",
            capacidadMaxima=2,
            descripcion="Vista ciudad",
            imagenes=["img1.jpg"],
            tipo_habitacion="deluxe",
            tipo_cama=["king"],
            tamano_habitacion="35m2",
            amenidades=["AC", "IDK"]
        ),
        Habitacion(
            id="22222222-2222-2222-2222-000000000002",
            hotelId="11111111-1111-1111-1111-000000000001",
            tipo="Doble",
            categoria="Deluxe",
            capacidadMaxima=2,
            descripcion="Vista ciudad",
            imagenes=["img1.jpg"],
            tipo_habitacion="deluxe",
            tipo_cama=["king"],
            tamano_habitacion="35m2",
            amenidades=["AC", "IDK"]
        ),
        Habitacion(
            id="22222222-2222-2222-2222-000000000003",
            hotelId="11111111-1111-1111-1111-000000000002",
            tipo="Doble",
            categoria="Deluxe",
            capacidadMaxima=2,
            descripcion="Vista ciudad",
            imagenes=["img1.jpg"],
            tipo_habitacion="deluxe",
            tipo_cama=["king"],
            tamano_habitacion="35m2",
            amenidades=["AC", "IDK"]
        ),
        Habitacion(
            id="22222222-2222-2222-2222-000000000004",
            hotelId="11111111-1111-1111-1111-000000000002",
            tipo="Doble",
            categoria="Deluxe",
            capacidadMaxima=3,
            descripcion="Vista ciudad",
            imagenes=["img1.jpg"],
            tipo_habitacion="deluxe",
            tipo_cama=["king"],
            tamano_habitacion="35m2",
            amenidades=["AC", "IDK"]
        ),
    ]

    session.add_all(habitaciones)
    session.commit()


    # TARIFAS
    tarifas = [
        Tarifa(
            id="55555555-5555-5555-5555-000000000001",
            habitacionId="22222222-2222-2222-2222-000000000001",
            precioBase=100.0,
            moneda="EUR",
            fechaInicio=datetime(2024, 4, 1),
            fechaFin=datetime(2028, 4, 30),
            descuento=0.1,
        ),
        Tarifa(
            id="55555555-5555-5555-5555-000000000002",
            habitacionId="22222222-2222-2222-2222-000000000002",
            precioBase=150.0,
            moneda="EUR",
            fechaInicio=datetime(2024, 4, 1),
            fechaFin=datetime(2028, 4, 30),
            descuento=0.0,
        ),
        Tarifa(
            id="55555555-5555-5555-5555-000000000003",
            habitacionId="22222222-2222-2222-2222-000000000003",
            precioBase=80.0,
            moneda="EUR",
            fechaInicio=datetime(2024, 4, 1),
            fechaFin=datetime(2028, 4, 30),
            descuento=0.0,
        ),
        Tarifa(
            id="55555555-5555-5555-5555-000000000004",
            habitacionId="22222222-2222-2222-2222-000000000004",
            precioBase=400.0,
            moneda="EUR",
            fechaInicio=datetime(2024, 4, 1),
            fechaFin=datetime(2028, 4, 30),
            descuento=0.2,
        ),
    ]
    session.add_all(tarifas)
    session.commit()


    # RESERVAS
    reservas = [
        Reserva(
            id="33333333-3333-3333-3333-000000000001",
            codigo="CODE1",
            viajeroId="44444444-4444-4444-4444-000000000001",
            habitacionId="22222222-2222-2222-2222-000000000001",
            fechaCheckIn=datetime(2026, 9, 1, 15, 0),
            fechaCheckOut=datetime(2026, 9, 3, 10, 0),
            numHuespedes=2,
            estado="CONFIRMADA",
            subtotal=200.0,
            impuestos=40.0,
            total=240.0,
            moneda="EUR",
        ),
        Reserva(
            id="33333333-3333-3333-3333-000000000002",
            codigo="CODE2",  
            viajeroId="44444444-4444-4444-4444-000000000002",
            habitacionId="22222222-2222-2222-2222-000000000003",
            fechaCheckIn=datetime(2026, 8, 1, 15, 0),
            fechaCheckOut=datetime(2026, 8, 3, 10, 0),
            numHuespedes=2,
            estado="CONFIRMADA",
            subtotal=200.0,
            impuestos=40.0,
            total=240.0,
            moneda="EUR",
        ),
    ]
    session.add_all(reservas)
    session.commit()

    resenas = [
        Resena(
            id="66666666-6666-6666-6666-000000000001",
            viajeroId="77777777-7777-7777-7777-000000000001",
            hotelId="11111111-1111-1111-1111-000000000001",
            reservaId="33333333-3333-3333-3333-000000000001",
            calificacion=4,
            comentario="Buena",
            fecha=datetime(2026, 8, 1, 15, 0),
            verificada=True
        ),
        Resena(
            id="66666666-6666-6666-6666-000000000002",
            viajeroId="77777777-7777-7777-7777-000000000001",
            hotelId="11111111-1111-1111-1111-000000000001",
            reservaId="33333333-3333-3333-3333-000000000001",
            calificacion=3,
            comentario="Buena",
            fecha=datetime(2026, 8, 1, 15, 0),
            verificada=True
        ),   
    ]
    session.add_all(resenas)
    session.commit()
    
    session.close()

    print("DB inicializada con datos mock")