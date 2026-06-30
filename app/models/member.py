import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship

from app.database import Base


class MemberStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    turf_id = Column(Integer, ForeignKey("turfs.id"), nullable=False)
    membership_id = Column(Integer, ForeignKey("memberships.id"), nullable=False)

    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=False, index=True)

    amount_paid = Column(Float, nullable=False)
    transaction_id = Column(String, nullable=False)

    status = Column(Enum(MemberStatus), default=MemberStatus.PENDING, nullable=False)
    starts_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    turf = relationship("Turf", back_populates="members")
    membership = relationship("Membership", back_populates="members")
