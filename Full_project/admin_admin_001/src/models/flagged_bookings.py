# # src/models/flagged_bookings.py
# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
# from sqlalchemy.orm import relationship
# from src.common.database import Base
# import enum


# class FlagStatus(str, enum.Enum):
#     pending = "pending"
#     reviewed = "reviewed"
#     resolved = "resolved"


# class FlaggedBooking(Base):
#     __tablename__ = "flagged_bookings"

#     id = Column(Integer, primary_key=True, index=True)

#     # Foreign keys
#     booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)
#     provider_id = Column(Integer, ForeignKey("providers.provider_id"), nullable=False)

#     # Metadata
#     reason = Column(String, nullable=False)
#     status = Column(Enum(FlagStatus), nullable=False, default=FlagStatus.pending)

#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     resolved_at = Column(DateTime(timezone=True), nullable=True)

#     # Relationships
#     provider = relationship("Provider", back_populates="flagged_bookings")
#     booking = relationship("Booking", back_populates="flagged_bookings")




from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.common.database import Base
from datetime import datetime

class FlaggedBooking(Base):
    __tablename__ = "flagged_bookings"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.provider_id"), nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    provider = relationship("Provider", back_populates="flagged_bookings")
