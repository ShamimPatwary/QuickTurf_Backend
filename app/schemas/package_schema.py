from typing import List, Optional

from pydantic import BaseModel


class PackageCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    sport_ids: List[int] = []


class PackageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
    sport_ids: Optional[List[int]] = None


class PackageSportOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PackageOut(BaseModel):
    id: int
    turf_id: int
    name: str
    description: Optional[str]
    price: float
    is_active: bool
    sports: List[PackageSportOut] = []

    class Config:
        from_attributes = True
