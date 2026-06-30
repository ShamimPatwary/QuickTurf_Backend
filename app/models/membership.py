from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean, DateTime, Table, func
from sqlalchemy.orm import relationship

from app.database import Base

membership_sports = Table(
    "membership_sports",
    Base.metadata,
    Column("membership_id", Integer, ForeignKey("memberships.id"), primary_key=True),
    Column("sport_id", Integer, ForeignKey("sports.id"), primary_key=True),
)


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    turf_id = Column(Integer, ForeignKey("turfs.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_days = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    discount_percentage = Column(Float, default=0, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    turf = relationship("Turf", back_populates="memberships")
    sports = relationship("Sport", secondary=membership_sports, back_populates="memberships")
    members = relationship("Member", back_populates="membership", cascade="all, delete-orphan")
