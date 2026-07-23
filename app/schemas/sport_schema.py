from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SportCreate(BaseModel):
    name: str


class SportUpdate(BaseModel):
    name: Optional[str] = None


class SportOut(BaseModel):
    id: int
    turf_id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
