from typing import List, Optional

from fastapi import HTTPException, status

from app.models.booking import Booking, PaymentStatus
from app.models.turf import TurfStatus
from app.patterns.factories.booking_factory import BookingFactory
from app.patterns.observers import booking_subject
from app.repositories.booking_repository import BookingRepository
from app.repositories.member_repository import MemberRepository
from app.repositories.sport_repository import SportRepository
from app.repositories.time_slot_repository import TimeSlotRepository
from app.repositories.turf_repository import TurfRepository
from app.schemas.booking_schema import BookingUpdate, PublicBookingCreate
from app.services.base_service import BaseService


class BookingService(BaseService):
    """Business logic for creating and managing bookings, wired to Factory + Observer patterns."""

    def __init__(self, db):
        super().__init__(db)
        self.booking_repo = BookingRepository(db)
        self.sport_repo = SportRepository(db)
        self.time_slot_repo = TimeSlotRepository(db)
        self.turf_repo = TurfRepository(db)
        self.member_repo = MemberRepository(db)