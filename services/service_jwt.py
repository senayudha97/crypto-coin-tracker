from datetime import datetime, timedelta
from typing import Union
from fastapi import HTTPException

from jose import JWTError, jwt

from dto.dto_common import TokenData


class ServiceJwt:
    def __init__(self) -> None:
        self.SECRET_KEY = "39d4f3e0a3456e9be59bd92f7632a862"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.blacklisted_tokens = set()

    def create_access_token(
        self, data: dict, expires_delta: Union[timedelta, None] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

