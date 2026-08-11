from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.time_slot import TimeSlot


def lock_and_validate_slot(db: Session, time_slot_id: int, booking_date: date) -> TimeSlot:
    """
    Locks the time slot row (SELECT ... FOR UPDATE) and ensures no active booking
    already exists for the same slot and date, preventing race-condition double bookings.
    """
    stmt = select(TimeSlot).where(TimeSlot.id == time_slot_id).with_for_update()
    time_slot = db.execute(stmt).scalar_one_or_none()

    if not time_slot or not time_slot.is_active:
        raise NoResultFound("Time slot not available")

    existing = (
        db.query(Booking)
        .filter(
            Booking.time_slot_id == time_slot_id,
            Booking.booking_date == booking_date,
            Booking.status != BookingStatus.CANCELLED,
        )
        .with_for_update()
        .first()
    )
    if existing:
        raise ValueError("This slot is already booked for the selected date")

    return time_slot
