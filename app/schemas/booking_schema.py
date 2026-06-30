from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.booking import BookingStatus, PaymentStatus, MatchType


class PublicBookingCreate(BaseModel):
    turf_id: int
    sport_id: int
    time_slot_id: int
    booking_date: date
    customer_name: str
    customer_phone: str
    customer_email: Optional[EmailStr] = None
    paid_amount: float = 0
    notes: Optional[str] = None
    match_type: MatchType = MatchType.FRIENDLY
    transaction_id: Optional[str] = None


class BookingUpdate(BaseModel):
    booking_date: Optional[date] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    notes: Optional[str] = None
    status: Optional[BookingStatus] = None
    match_type: Optional[MatchType] = None


class BookingAddPayment(BaseModel):
    amount: float
    method: Optional[str] = None
    transaction_id: Optional[str] = None


class BookingOut(BaseModel):
    id: int
    turf_id: int
    sport_id: int
    sport_name: Optional[str] = None
    time_slot_id: int
    customer_name: str
    customer_phone: str
    customer_email: Optional[str]
    booking_date: date
    notes: Optional[str]
    match_type: MatchType
    total_amount: float
    discount_amount: float
    paid_amount: float
    due_amount: float
    transaction_id: Optional[str]
    status: BookingStatus
    payment_status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_matches: int
    total_match_amount: float
    paid_amount: float
    due_amount: float
    upcoming_matches: int
    completed_matches: int
    cancelled_matches: int
    payment_paid: int
    payment_partial: int
    payment_pending: int
    total_revenue: float
    total_discount_given: float
    active_members: int
    pending_members: int
