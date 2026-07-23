from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, index=True)
    turf_id = Column(Integer, ForeignKey("turfs.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    turf = relationship("Turf", back_populates="sports")
    time_slots = relationship("TimeSlot", back_populates="sport", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="sport")
    packages = relationship("Package", secondary="package_sports", back_populates="sports")
    memberships = relationship("Membership", secondary="membership_sports", back_populates="sports")
