from fastapi import FastAPI

from src.api.routers import health, task, user, auth


def register_routers(app: FastAPI) -> None:
    app.include_router(health.router, tags=["Health"])
    app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
    app.include_router(user.router, prefix="/users", tags=["Users"])
    app.include_router(auth.auth_router, prefix="/auth", tags=["Auth"])
