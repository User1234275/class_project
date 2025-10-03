# # src/models/bookings.py
# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
# from sqlalchemy.orm import relationship
# from src.common.database import Base


# class Booking(Base):
#     __tablename__ = "bookings"

#     booking_id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, nullable=False)       # assuming a user FK
#     provider_id = Column(Integer, ForeignKey("providers.provider_id"), nullable=False)
#     service_details = Column(String, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     # Relationships
#     provider = relationship("Provider")
#     flagged_bookings = relationship("FlaggedBooking", back_populates="booking")


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.common.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.provider_id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("Provider")
