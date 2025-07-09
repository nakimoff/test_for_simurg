from fastapi import FastAPI
from src.api.routers import register_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Simurg Task API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    register_routers(app)

    return app
