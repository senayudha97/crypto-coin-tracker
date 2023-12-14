from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from enums.enum_method import Method
from enums.enum_tipe import Tipe
from models.model_common import PyObjectId

class Transaction(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    tipe: Tipe
    amount: int = 5000
    notes: Optional[str] = None
    method: Method

    class Config:
        json_encoders = {ObjectId : str}