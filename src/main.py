from os import getenv

import uvicorn

REPOSITORY_IMPL = getenv("REPOSITORY_IMPL", "memory")
APP_HOST = getenv("APP_HOST", "0.0.0.0")
APP_PORT = getenv("APP_PORT", "8000")

if __name__ == "__main__":
    uvicorn.run("entrypoints.app:app", host=APP_HOST, port=int(APP_PORT))