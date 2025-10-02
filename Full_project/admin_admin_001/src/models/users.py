from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from src.common.database import Base
import enum

class UserRole(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(Enum(UserRole), default=UserRole.buyer)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
