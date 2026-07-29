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

    def booked_slot_ids(self, sport_id: int, booking_date: date) -> set:
        rows = (
            self.db.query(Booking)
            .filter(
                Booking.sport_id == sport_id,
                Booking.booking_date == booking_date,
                Booking.status != BookingStatus.CANCELLED,
            )
            .all()
        )
        return {b.time_slot_id for b in rows}
    
    def add_payment(self, booking_id: int, amount: float, method: Optional[str], transaction_id: Optional[str] = None) -> Payment:
        payment = Payment(booking_id=booking_id, amount=amount, method=method, transaction_id=transaction_id)
        self.db.add(payment)
        self.db.flush()
        return payment
    
    def turf_aggregate_counts(self, turf_id: int) -> dict:
        base_query = self.db.query(Booking).filter(Booking.turf_id == turf_id)

        return {
            "total_matches": base_query.count(),
            "total_match_amount": base_query.with_entities(
                func.coalesce(func.sum(Booking.total_amount), 0)
            ).scalar(),
            "paid_amount": base_query.with_entities(
                func.coalesce(func.sum(Booking.paid_amount), 0)
            ).scalar(),
            "due_amount": base_query.with_entities(
                func.coalesce(func.sum(Booking.due_amount), 0)
            ).scalar(),
            "upcoming_matches": base_query.filter(Booking.status == BookingStatus.UPCOMING).count(),
            "completed_matches": base_query.filter(Booking.status == BookingStatus.COMPLETED).count(),
            "cancelled_matches": base_query.filter(Booking.status == BookingStatus.CANCELLED).count(),
            "payment_paid": base_query.filter(Booking.payment_status == PaymentStatus.PAID).count(),
            "payment_partial": base_query.filter(Booking.payment_status == PaymentStatus.PARTIAL).count(),
            "payment_pending": base_query.filter(Booking.payment_status == PaymentStatus.PENDING).count(),
            "total_discount_given": base_query.with_entities(
                func.coalesce(func.sum(Booking.discount_amount), 0)
            ).scalar(),
            "active_members": self.db.query(Member)
            .filter(Member.turf_id == turf_id, Member.status == MemberStatus.ACTIVE)
            .count(),
            "pending_members": self.db.query(Member)
            .filter(Member.turf_id == turf_id, Member.status == MemberStatus.PENDING)
            .count(),
        }
