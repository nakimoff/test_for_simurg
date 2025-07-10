from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt, JWTError
from src.schemas.token import TokenData
from src.core.config import settings


class TokenService:
    SECRET_KEY: str = settings.JWT_SECRET_KEY
    ALGORITHM: str = settings.JWT_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def create_access_token(
        cls,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        to_encode: Dict[str, Any] = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_access_token(cls, token: str) -> TokenData:
        try:
            payload: Dict[str, Any] = jwt.decode(
                token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM]
            )
            user_id_str = payload.get("sub")
            if user_id_str is None:
                raise JWTError("Token missing subject (sub)")
            user_id = int(user_id_str)
            return TokenData(user_id=user_id)
        except (JWTError, ValueError, TypeError):
            raise JWTError("Invalid token")
