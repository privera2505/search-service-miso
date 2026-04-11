# Search App

Microservicio encargado de buscar habitaciones disponibles. Implementando Python 3 + FastAPI, busqueda en PostgreSQL y empaquetado en Docker. Expone endpoints para consultar las habitaciones disponibles.
## Índice

1. [Estructura](#estructura)
2. [Variables de entorno](#variables-de-entorno)
3. [Query Parameters](#query-parameters)
4. [Ejecución](#ejecución)
5. [Documentación Endpoints](#documentación-endpoints)
6. [Autor](#autor)

## Estructura

Estructura de la **carpeta de la aplicación** (`posts_app/`):
```
search_app/
├─ Dockerfile                               # Imagen de la app (uvicorn + FastAPI)
├─ .dockerignore & .gitignore               # Excluye tests, .venv, __pycache__, etc.
├─ requirements.txt                         # dependencias
├─ src/
│  ├─ error.py
│  ├─ config.py                             # Variables de ambiente       
│  ├─ main.py                               # Arranque de uvicorn
│  ├─ domain/
│  │  ├─ models/
│  │  │  └─ models.py                       # Entidades
│  │  ├─ ports/
│  │  │  └─ search_repository_port.py        # Contrato del repositorio
│  │  └─ use_cases/
│  ├─ adapters/
│  │  ├─ memory/                            # Repo en memoria (tests / desarrollo)
│  │  └─ postgres/                          # Repo PostgreSQL (Prod)
│  └─ entrypoints/
│     ├─ assembly.py                        # Inyección de dependencias (memory|postgres)
│     └─ App.py                             # Endpoints
└─ tests/                                   # Carpeta para pruebas
```

## Variables de Entorno

Estas variables permiten configurar el comportamiento de la aplicación según el entorno y la infraestructura utilizada.

---

### Configuración General

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `APP_HOST` | string | `0.0.0.0` | Host donde se expone la aplicación. |
| `APP_PORT` | string | `8000` | Puerto en el que corre la aplicación. |

---

### Repositorio de Datos

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `REPOSITORY_IMPL` | string | `memory` | Define la implementación del repositorio. Puede ser: <br> - `memory`: usa datos en memoria. <br> - `postgres`: usa base de datos en GCP (Cloud SQL). |

---

### Entorno de Ejecución
Cuando el `REPOSITORY_IMPL` es `postgres` tener en cuenta lo siguiente:
| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `ENVIRONMENT` | string | `dev` | Define el entorno de ejecución. <br><br> - `dev`: usar cuando se conecta desde un computador local utilizando el proxy de Cloud SQL. <br> - `prod` o `test`: usar cuando la aplicación se despliega en la nube sin proxy local. |

---

### Configuración de Base de Datos (PostgreSQL)

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `INSTANCE_CONNECTION_NAME` | string | `secret-lambda-491419-p2:us-central1:test-search-services` | Nombre de la instancia de Cloud SQL en GCP. |
| `DB_HOST` | string | `localhost` | Host de la base de datos. |
| `DB_PORT` | string | `5432` | Puerto de la base de datos. |
| `DB_USER` | string | `postgres` | Usuario de la base de datos. |
| `DB_PASSWORD` | string | `Postgres1.` | Contraseña de la base de datos. |
| `DB_NAME` | string | `postgres` | Nombre de la base de datos. |

---

### CORS

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `ALLOWED_ORIGINS` | string | `*` | Lista de orígenes permitidos para CORS. <br><br> Debe especificarse como una cadena de texto separada por espacios. <br> Ejemplo: <br> `http://localhost:3000 https://miapp.com` |

---

### Notas

- Si `REPOSITORY_IMPL=postgres`, asegúrate de configurar correctamente las variables de base de datos.
- En entorno `dev`, es necesario usar el proxy de Cloud SQL para conexiones locales.
- `ALLOWED_ORIGINS` se procesa como lista usando `.split()`, por lo que los valores deben separarse con espacios.

## Query Parameters

| Parámetro | Tipo | Requerido | Descripción |
|----------|------|----------|-------------|
| `ciudad` | string | Sí | Ciudad donde se desea buscar alojamiento. Ejemplo: `Madrid`. |
| `checkin` | date (YYYY-MM-DD) | Sí | Fecha de entrada al alojamiento. |
| `checkout` | date (YYYY-MM-DD) | Sí | Fecha de salida del alojamiento. Debe ser posterior al check-in. |
| `group` | integer | Sí | Número de personas que se hospedarán. |
| `rooms` | integer | Sí | Número de habitaciones requeridas. |

### Consideraciones
- Las fechas deben estar en formato YYYY-MM-DD.
- checkout debe ser mayor que checkin.
- group y rooms deben ser valores positivos.
- La disponibilidad depende de las reservas existentes en el sistema.

### Ejemplo de uso

```http
GET /search/search_rooms?ciudad=Madrid&checkin=2026-10-01&checkout=2026-10-12&group=1&rooms=1
```
---

## Ejecución

### C) Desarrollo local con pip
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

## Documentación Endpoints

### API Endpoints

- `GET /posts` - Consultar habitaciones disponibles

### Probar EndPoints

### **1. Consultar habitaciones**
**Descripción:** consulta las habitaciones de un hotel teniendo en cuenta una seria de parametros

```bash
curl --location 'http://localhost:8000/search/search_rooms?ciudad=Madrid&checkin=2026-10-01&checkout=2026-10-12&group=1&rooms=1'
```
**Respuesta Esperada:** 
- Status: 200 OK
- Body: [
    {
        "id": "22222222-2222-2222-2222-000000000001",
        "nombre_hotel": "Hotel 1",
        "precio": 990.0,
        "direccion": "Calle 123",
        "capacidad_maxima": 2,
        "distancia": "3 km del centro",
        "acceso": "Metro",
        "estrellas": 5,
        "puntuacion_resena": 3.5,
        "cantidad_resenas": 2,
        "tipo_habitacion": "Deluxe",
        "tipo_cama": [
            "king"
        ],
        "tamano_habitacion": "35m2",
        "amenidades": [
            "AC",
            "IDK"
        ],
        "imagenes": [
            "img1.jpg"
        ]
    }
]

### **2. Consultar habitaciones con fechacheckin mayor o igual a fechacheckout**
**Descripción:** consulta las habitaciones de un hotel, pero la fecha de checkin es superior a la fecha checkout

```bash
curl --location 'http://localhost:8000/search/search_rooms?ciudad=Madrid&checkin=2026-11-01&checkout=2026-10-12&group=1&rooms=1'
```
**Respuesta Esperada:** 
- Status: 400
- Body: the check-in date is later than the check-out date

### **3. Consultar habitaciones con fechacheckin menor a la fecha actual**
**Descripción:** consulta las habitaciones de un hotel, pero la fecha de checkin es menor que la fecha actual

```bash
curl --location 'http://localhost:8000/search/search_rooms?ciudad=Madrid&checkin=2010-11-01&checkout=2010-10-12&group=1&rooms=1'
```
**Respuesta Esperada:** 
- Status: 400
- Body: the check-in date is lower than today

### **4. Consultar habitaciones con parametros invalidos**
**Descripción:** consulta las habitaciones de un hotel, pero usando alguna fecha sin el formato establecido.

```bash
curl --location 'http://localhost:8000/search/search_rooms?ciudad=Madrid&checkin=11-01-2025&checkout=2010-10-12&group=1&rooms=1'
```
**Respuesta Esperada:** 
- Status: 422

### **5. Consultar habitaciones con parametros invalidos**
**Descripción:** consulta las habitaciones de un hotel, pero usando en group una letra.

```bash
curl --location 'http://localhost:8000/search/search_rooms?ciudad=Madrid&checkin=2026-10-01&checkout=2026-10-12&group=f&rooms=1'
```
**Respuesta Esperada:** 
- Status: 422

### **6. Health Check del Servicio**
**Descripción:**  Verifica el estado del servicio
```bash
curl 'http://localhost:8000/search/ping'
```
**Respuesta Esperada:** 
- Status: 200 OK
- "pong"

### **7. Consultar las ciudades donde hay hoteles**
**Descripción:**  Devuelve una lista de ciudades únicas en las que existen hoteles activos.
```bash
curl 'http://localhost:8000/search/search_cities'
```
**Respuesta Esperada:** 
- Status: 200
- ["Madrid"]

## Autor

- Pablo Jose Rivera herrera
- Contacto: `<p.riverah@uniandes.edu.co>`