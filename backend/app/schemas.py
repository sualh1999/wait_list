from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

class WaitlistCreate(BaseModel):
    email: EmailStr

class WaitlistOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
