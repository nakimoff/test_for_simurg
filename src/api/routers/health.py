from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/ping", summary="Health check")
async def ping() -> JSONResponse:
    return JSONResponse(content={"message": "pong"})
