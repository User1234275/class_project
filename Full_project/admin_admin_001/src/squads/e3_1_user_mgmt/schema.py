from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserOut(BaseModel):
    id: int = Field(..., alias="user_id")
    name: str
    email: str
    status: str
    role: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class UsersListResponse(BaseModel):
    users: List[UserOut]
    meta: dict

class SuspendRestoreRequest(BaseModel):
    reason: Optional[str] = Field(None, description="Optional reason for action")

class ActionResponse(BaseModel):
    message: str
    user: UserOut
