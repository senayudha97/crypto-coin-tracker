from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dto.dto_common import StandardResponse

from dto.dto_user import InputLogin, InputUser, OutputLogin
from services.service_user import ServiceUser

router_user = APIRouter(prefix="/api", tags=["User"])

@router_user.post("/user")
def signup_user(input_user: InputUser, service_user: ServiceUser = Depends()):
    service_user.insert_new_user(input_user)
    return StandardResponse(detail="User created")

@router_user.post("/login")
def signin_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service_user: ServiceUser = Depends()):
    jwt_token = service_user.login_user(InputLogin(username=form_data.username, password=form_data.password))
    
    return OutputLogin(access_token=jwt_token)
