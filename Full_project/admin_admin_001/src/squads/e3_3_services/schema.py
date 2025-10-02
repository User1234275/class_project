from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class FlagStatus(str, Enum):
    pending = "pending"
    reviewed = "reviewed"
    resolved = "resolved"

class FlaggedBookingOut(BaseModel):
    id: int
    booking_id: int
    provider_id: int
    reason: str
    status: FlagStatus
    created_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        orm_mode = True

class AdminActionPayload(BaseModel):
    admin_id: int = Field(..., example=101)
    reason: str = Field(..., min_length=1)
