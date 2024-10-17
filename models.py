from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Contact(BaseModel):
    id: Optional[str] = None  
    name: str
    email: str
    phone: str

    class Config:
        # Use this to handle ObjectId serialization
        json_encoders = {
            ObjectId: str
        }
