from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from src.common.database import Base

class Marketplace(Base):
    __tablename__ = "marketplace"

    listing_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Alias for compatibility with code expecting MarketplaceListing
MarketplaceListing = Marketplace
