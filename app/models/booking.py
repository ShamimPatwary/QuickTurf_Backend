import enum

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Date, Enum, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class BookingStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, enum.Enum):
    PAID = "paid"
    PARTIAL = "partial"
    PENDING = "pending"


class MatchType(str, enum.Enum):
    FRIENDLY = "friendly"
    PRACTICE = "practice"
    TOURNAMENT = "tournament"
    LEAGUE = "league"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    turf_id = Column(Integer, ForeignKey("turfs.id"), nullable=False)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    time_slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False)

    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_email = Column(String, nullable=True)

    booking_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    match_type = Column(Enum(MatchType), default=MatchType.FRIENDLY, nullable=False)

    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    paid_amount = Column(Float, default=0)
    due_amount = Column(Float, default=0)
    transaction_id = Column(String, nullable=True)

    status = Column(Enum(BookingStatus), default=BookingStatus.UPCOMING, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    turf = relationship("Turf", back_populates="bookings")
    sport = relationship("Sport", back_populates="bookings")
    time_slot = relationship("TimeSlot", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")

    @property
    def sport_name(self) -> str | None:
        return self.sport.name if self.sport else None
