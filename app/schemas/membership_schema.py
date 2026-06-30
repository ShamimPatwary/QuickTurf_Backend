from typing import List, Optional

from pydantic import BaseModel


class MembershipCreate(BaseModel):
    name: str
    description: Optional[str] = None
    duration_days: int
    price: float
    discount_percentage: float = 0
    sport_ids: List[int] = []


class MembershipUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[float] = None
    discount_percentage: Optional[float] = None
    is_active: Optional[bool] = None
    sport_ids: Optional[List[int]] = None


class MembershipSportOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MembershipOut(BaseModel):
    id: int
    turf_id: int
    name: str
    description: Optional[str]
    duration_days: int
    price: float
    discount_percentage: float
    is_active: bool
    sports: List[MembershipSportOut] = []

    class Config:
        from_attributes = True
