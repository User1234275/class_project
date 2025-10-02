from sqlalchemy import Column, Integer, String, DateTime, func
from src.common.database import Base

class Provider(Base):
    __tablename__ = "providers"

    provider_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
