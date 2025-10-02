from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from src.common.database import Base

from enum import Enum

class Dispute(Base):
    __tablename__ = "disputes"

    dispute_id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("marketplace.listing_id"))
    raised_by = Column(Integer, ForeignKey("users.user_id"))
    status = Column(String, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Alias for compatibility with code expecting PaymentDispute
PaymentDispute = Dispute

# DisputeStatus enum for status field
class DisputeStatus(str, Enum):
    open = "open"
    resolved = "resolved"
    closed = "closed"
