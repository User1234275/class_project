from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from src.common.database import Base

class FlaggedListing(Base):
    __tablename__ = "flagged_listings"

    flag_id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("marketplace.listing_id"))
    reason = Column(String, nullable=False)
    flagged_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
