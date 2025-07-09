from fastapi import FastAPI
from src.api.routers import task

app = FastAPI(title="Simurg Task API")

app.include_router(task.router, prefix="/tasks", tags=["Tasks"])


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}
