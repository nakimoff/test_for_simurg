from fastapi import FastAPI

app = FastAPI(title="Simurg Task API")


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}
