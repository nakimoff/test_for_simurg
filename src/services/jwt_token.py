from datetime import datetime, timedelta
from jose import jwt, JWTError
from src.schemas.token import TokenData
from src.core.config import settings


class TokenService:
    SECRET_KEY = settings.JWT_SECRET_KEY
    ALGORITHM = settings.JWT_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    @classmethod
    def create_access_token(
        cls, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_access_token(cls, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            user_id = int(payload.get("sub"))
            return TokenData(user_id=user_id)
        except (JWTError, ValueError, TypeError):
            raise JWTError("Invalid token")
