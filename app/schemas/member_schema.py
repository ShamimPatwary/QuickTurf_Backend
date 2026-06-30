from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.member import MemberStatus


class MemberPurchaseCreate(BaseModel):
    membership_id: int
    name: str
    email: Optional[EmailStr] = None
    phone: str
    amount_paid: float
    transaction_id: str


class MemberStatusUpdate(BaseModel):
    status: MemberStatus


class MemberOut(BaseModel):
    id: int
    turf_id: int
    membership_id: int
    name: str
    email: Optional[str]
    phone: str
    amount_paid: float
    transaction_id: str
    status: MemberStatus
    starts_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class MembershipCheckResult(BaseModel):
    is_member: bool
    discount_percentage: float = 0
    membership_name: Optional[str] = None
