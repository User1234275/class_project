from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from src.common.database import Base

class AdminAction(Base):
    __tablename__ = "admin_actions"

    action_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.user_id"))
    action_type = Column(String, nullable=False)
    target_id = Column(Integer, nullable=True)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
