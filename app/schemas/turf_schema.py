from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.models.turf import TurfStatus


class TurfImageOut(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True


class TurfCreate(BaseModel):
    name: str
    details: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    google_map_link: Optional[str] = None
    turf_admin_email: EmailStr
    turf_admin_password: str


class TurfUpdate(BaseModel):
    name: Optional[str] = None
    details: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    google_map_link: Optional[str] = None


class TurfStatusUpdate(BaseModel):
    status: TurfStatus
    subscription_due_date: Optional[datetime] = None


class TurfOut(BaseModel):
    id: int
    name: str
    details: Optional[str]
    address: str
    latitude: Optional[float]
    longitude: Optional[float]
    google_map_link: Optional[str]
    status: TurfStatus
    subscription_due_date: Optional[datetime]
    created_at: datetime
    images: List[TurfImageOut] = []

    class Config:
        from_attributes = True


class TurfPublicOut(BaseModel):
    id: int
    name: str
    details: Optional[str]
    address: str
    latitude: Optional[float]
    longitude: Optional[float]
    google_map_link: Optional[str]
    images: List[TurfImageOut] = []

    class Config:
        from_attributes = True
