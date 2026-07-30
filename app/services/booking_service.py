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
    
    def create_public_booking(self, data: PublicBookingCreate) -> Booking:
        turf = self.turf_repo.get_by_id(data.turf_id)
        if not turf or turf.status != TurfStatus.ACTIVE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Turf not available for booking")

        sport = self.sport_repo.get_by_turf(data.sport_id, data.turf_id)
        if not sport:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sport not found for this turf")

        time_slot = self.time_slot_repo.get_locked(data.time_slot_id)
        if not time_slot or not time_slot.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Time slot not available")

        if self.booking_repo.has_conflicting_booking(data.time_slot_id, data.booking_date):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This slot is already booked for the selected date",
            )

        # Automatic membership discount: looked up by phone number, scoped to this turf and sport.
        active_member = self.member_repo.find_active_by_phone(data.turf_id, data.customer_phone, data.sport_id)
        discount_percentage = active_member.membership.discount_percentage if active_member else 0

        booking = BookingFactory.create_booking(
            turf_id=data.turf_id,
            sport_id=data.sport_id,
            time_slot=time_slot,
            booking_date=data.booking_date,
            customer_name=data.customer_name,
            customer_phone=data.customer_phone,
            customer_email=data.customer_email,
            paid_amount=data.paid_amount,
            notes=data.notes,
            match_type=data.match_type,
            transaction_id=data.transaction_id,
            discount_percentage=discount_percentage,
        )

        self.booking_repo.add(booking)

        if booking.paid_amount > 0:
            self.booking_repo.add_payment(booking.id, booking.paid_amount, "initial", data.transaction_id)

        self.booking_repo.commit()
        self.booking_repo.refresh(booking)

        booking_subject.notify_created(booking)

        return booking

    def list_turf_bookings(self, turf_id: int) -> List[Booking]:
        return self.booking_repo.list_by_turf(turf_id)