from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from src.common.database import Base

class FlagStatus(str, Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    REJECTED = "rejected"


# Example FlaggedTransaction model for flagged payments
class FlaggedTransaction(Base):
    __tablename__ = "flagged_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, nullable=False)
    flagged_by = Column(Integer, ForeignKey("users.user_id"))
    status = Column(String, default=FlagStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
