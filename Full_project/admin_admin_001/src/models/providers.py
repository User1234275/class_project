# from sqlalchemy import Column, Integer, String, DateTime, func
# from src.common.database import Base

# # class Provider(Base):
# #     __tablename__ = "providers"

# #     provider_id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String, nullable=False)
# #     service_type = Column(String, nullable=False)
# #     status = Column(String, nullable=False, default="active")
# #     created_at = Column(DateTime(timezone=True), server_default=func.now())



# # src/models/providers.py
# from sqlalchemy.orm import relationship

# class Provider(Base):
#     __tablename__ = "providers"

#     provider_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     service_type = Column(String, nullable=False)
#     status = Column(String, nullable=False, default="active")
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     # backref
#     flagged_bookings = relationship("FlaggedBooking", back_populates="provider")


from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.common.database import Base

class Provider(Base):
    __tablename__ = "providers"

    provider_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    status = Column(String,default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to FlaggedBooking (use string to avoid import issues)
    flagged_bookings = relationship("FlaggedBooking", back_populates="provider")
