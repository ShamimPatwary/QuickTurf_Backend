import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Float, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class TurfStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class Turf(Base):
    __tablename__ = "turfs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    google_map_link = Column(String, nullable=True)
    status = Column(Enum(TurfStatus), default=TurfStatus.ACTIVE, nullable=False)
    subscription_due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    images = relationship("TurfImage", back_populates="turf", cascade="all, delete-orphan")
    turf_admin = relationship("TurfAdmin", back_populates="turf", uselist=False, cascade="all, delete-orphan")
    sports = relationship("Sport", back_populates="turf", cascade="all, delete-orphan")
    packages = relationship("Package", back_populates="turf", cascade="all, delete-orphan")
    memberships = relationship("Membership", back_populates="turf", cascade="all, delete-orphan")
    members = relationship("Member", back_populates="turf", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="turf", cascade="all, delete-orphan")


class TurfImage(Base):
    __tablename__ = "turf_images"

    id = Column(Integer, primary_key=True, index=True)
    turf_id = Column(Integer, ForeignKey("turfs.id"), nullable=False)
    image_url = Column(String, nullable=False)

    turf = relationship("Turf", back_populates="images")
