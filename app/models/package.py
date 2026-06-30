from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean, DateTime, Table, func
from sqlalchemy.orm import relationship

from app.database import Base

package_sports = Table(
    "package_sports",
    Base.metadata,
    Column("package_id", Integer, ForeignKey("packages.id"), primary_key=True),
    Column("sport_id", Integer, ForeignKey("sports.id"), primary_key=True),
)


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    turf_id = Column(Integer, ForeignKey("turfs.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    turf = relationship("Turf", back_populates="packages")
    sports = relationship("Sport", secondary=package_sports, back_populates="packages")
