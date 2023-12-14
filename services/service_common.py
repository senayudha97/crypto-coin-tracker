

from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from services import service_jwt
from dto.dto_common import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], service_jwt: service_jwt.ServiceJwt = Depends()):
    print(token)
    return TokenData.model_validate(service_jwt.decode_token(token))