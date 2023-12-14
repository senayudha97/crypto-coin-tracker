from typing import Optional
from fastapi import Depends, HTTPException
from dto.dto_common import TokenData
from dto.dto_user import InputLogin, InputUser

from services import service_security
from repository.repository_user import RepositoryUser
from services.service_common import get_current_user
from services.service_jwt import ServiceJwt

class ServiceUser:
    def __init__(self, repository_user : RepositoryUser = Depends(), service_jwt: ServiceJwt = Depends()) -> None:
        self.repository_user = repository_user
        self.service_security = service_security
        self.service_jwt = service_jwt
        
    def insert_new_user(self, input_user : InputUser):
        found_duplicate_username = self.repository_user.find_user_by_username(input_user.username)
        
        if found_duplicate_username is not None:
            raise HTTPException(status_code=400, detail="Duplicate Username")
        
        # confirm password
        if input_user.password != input_user.confirm_password:
            raise HTTPException(status_code=400, detail="Password not match")
        
        #HASH PASSWORD
        input_user.password = self.service_security.get_password_hash(input_user.password)
        return self.repository_user.insert_new_user(input_user)
        
    def login_user(self, input_login: InputLogin):
        found_user = self.repository_user.find_user_by_username(input_login.username)
        #if username not found
        if found_user is None:
            raise HTTPException(status_code=404, detail="Invalid username or password")
        
        if not self.service_security.verify_password(input_login.password, found_user.password):
            raise HTTPException(status_code=404, detail="Invalid username or password")

        #Generate JWT
        jwt_token = self.service_jwt.create_access_token(TokenData(userId=str(found_user.id), name=found_user.name).model_dump())        
        return jwt_token
    

        
        
        
        