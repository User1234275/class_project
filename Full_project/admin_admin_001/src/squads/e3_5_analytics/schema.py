from pydantic import BaseModel
from datetime import datetime

class DashboardMetric(BaseModel):
    id: int
    metric_name: str
    metric_value: int
    time_bucket: datetime
    class Config:
        orm_mode = True

class AuditLogOut(BaseModel):
    id: int
    admin_id: int
    action: str
    entity_type: str
    entity_id: int
    timestamp: datetime
    class Config:
        orm_mode = True

class UserActivitySummary(BaseModel):
    total_users: int
    active_users: int
    suspended_users: int

class MarketplaceStats(BaseModel):
    total_listings: int
    active_listings: int
    pending_listings: int

class DisputeSummary(BaseModel):
    total_disputes: int
    open_disputes: int
    resolved_disputes: int
