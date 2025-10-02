from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class FlagStatus(str, Enum):
    pending = "pending"
    reviewed = "reviewed"
    cleared = "cleared"


class DisputeStatus(str, Enum):
    open = "open"
    under_review = "under_review"
    resolved = "resolved"
    escalated = "escalated"


class FlaggedTransactionResponse(BaseModel):
    id: UUID
    transaction_id: UUID
    flagged_reason: str
    status: FlagStatus
    flagged_at: datetime

    class Config:
        orm_mode = True


class DisputeResolveRequest(BaseModel):
    resolution: str
    resolved_by: UUID


class DisputeResponse(BaseModel):
    id: UUID
    status: DisputeStatus
    resolved_at: Optional[datetime]

    class Config:
        orm_mode = True

class FlaggedResolveRequest(BaseModel):
    status: FlagStatus  # reviewed or cleared
    resolved_by: UUID
    note: str | None = None
