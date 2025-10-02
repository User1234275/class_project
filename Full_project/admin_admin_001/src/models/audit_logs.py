from sqlalchemy import Column, Integer, String, DateTime, func
from src.common.database import Base

from enum import Enum

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    actor = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    admin_id = Column(Integer, nullable=True)
    entity_id = Column(String, nullable=True)
    entity_type = Column(String, nullable=True)
    details = Column(String, nullable=True)
    

# Enum for action types in audit logs
class ActionType(str, Enum):
    dispute_resolved = "dispute_resolved"
    flag_created = "flag_created"
    flag_resolved = "flag_resolved"


# Model for materialized view (analytics dashboard)
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr

class AdminDashboardView(Base):
    __tablename__ = "admin_dashboard_view"
    __table_args__ = ({'extend_existing': True},)

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
