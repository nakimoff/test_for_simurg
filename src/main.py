from fastapi import FastAPI
from src.api.routers import task, user

app = FastAPI(title="Simurg Task API")

app.include_router(task.router)
app.include_router(user.router)


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}
