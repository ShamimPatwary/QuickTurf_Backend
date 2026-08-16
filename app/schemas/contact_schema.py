from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str


class ContactMessageOut(BaseModel):
    id: int
    name: str
    email: Optional[str]
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
