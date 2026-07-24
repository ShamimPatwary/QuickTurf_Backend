from sqlalchemy import Column, Integer, String, ForeignKey, Float, Time, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sport = relationship("Sport", back_populates="time_slots")
    bookings = relationship("Booking", back_populates="time_slot")
