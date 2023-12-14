from pydantic import BaseModel

class StandardResponse(BaseModel):
    detail : str
    
class TokenData(BaseModel):
    userId: str
    name: str