from datetime import date
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.booking import Booking, BookingStatus, PaymentStatus
from app.models.member import Member, MemberStatus
from app.models.payment import Payment
from app.repositories.base_repository import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    model = Booking

    def list_by_turf(self, turf_id: int) -> List[Booking]:
        return (
            self.db.query(Booking)
            .options(joinedload(Booking.sport))
            .filter(Booking.turf_id == turf_id)
            .order_by(Booking.booking_date.desc())
            .all()
        )

    def get_by_turf(self, booking_id: int, turf_id: int) -> Optional[Booking]:
        return (
            self.db.query(Booking)
            .options(joinedload(Booking.sport))
            .filter(Booking.id == booking_id, Booking.turf_id == turf_id)
            .first()
        )

    def list_all_ordered(self) -> List[Booking]:
        return (
            self.db.query(Booking)
            .options(joinedload(Booking.sport))
            .order_by(Booking.created_at.desc())
            .all()
        )

    def has_conflicting_booking(self, time_slot_id: int, booking_date: date) -> bool:
        existing = (
            self.db.query(Booking)
            .filter(
                Booking.time_slot_id == time_slot_id,
                Booking.booking_date == booking_date,
                Booking.status != BookingStatus.CANCELLED,
            )
            .with_for_update()
            .first()
        )
        return existing is not None