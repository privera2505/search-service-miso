from adapters.postgres.init_db import init_db
from config import (
    APP_HOST,
    REPOSITORY_IMPL,
    APP_PORT
)

import uvicorn

if __name__ == "__main__":
    #inicializar base de datos
    #if REPOSITORY_IMPL == "postgres":
    #    init_db()
    uvicorn.run("entrypoints.app:app", host=APP_HOST, port=int(APP_PORT))