# from pydantic import BaseModel, Field
# from typing import Optional
# from datetime import datetime

# class FlaggedListingOut(BaseModel):
#     id: int = Field(..., alias="flag_id")
#     listing_id: int
#     reason: str
#     status: str
#     created_at: datetime
#     resolved_at: Optional[datetime] = None
#     resolved_by: Optional[int] = None

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True

# class ResolveFlagIn(BaseModel):
#     resolved_by: int
#     notes: Optional[str] = None

# # class ResolveFlagOut(BaseModel):
# #     id: int
# #     status: str
# #     resolved_at: Optional[datetime]
# #     resolved_by: Optional[int]

# #     class Config:
# #         orm_mode = True


# class ResolveFlagOut(BaseModel):
#     id: int = Field(..., alias="flag_id")  # map flag_id → id
#     status: str
#     resolved_at: Optional[datetime]
#     resolved_by: Optional[int]

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True


# class DisputeOut(BaseModel):
#     id: int
#     user_id: int
#     listing_id: int
#     status: str
#     created_at: datetime
#     resolved_at: Optional[datetime]
#     resolved_by: Optional[int]
#     resolution_notes: Optional[str]

#     class Config:
#         orm_mode = True

# class ResolveDisputeIn(BaseModel):
#     resolved_by: int
#     resolution_notes: Optional[str] = None

# class ResolveDisputeOut(BaseModel):
#     id: int
#     status: str
#     resolved_at: Optional[datetime]
#     resolved_by: Optional[int]

#     class Config:
#         orm_mode = True

# class FlaggedListingCreate(BaseModel):
#     listing_id: int
#     reason: str
#     status: str = "pending"




from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# -----------------------
# Flagged Listings
# -----------------------
class FlaggedListingOut(BaseModel):
    flag_id: int = Field(..., alias="flag_id")  # Primary key in DB
    listing_id: int
    reason: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FlaggedListingCreate(BaseModel):
    listing_id: int
    reason: str
    status: str = "pending"


class ResolveFlagIn(BaseModel):
    resolved_by: int
    notes: Optional[str] = None


class ResolveFlagOut(BaseModel):
    flag_id: int = Field(..., alias="flag_id")  # matches returned dict
    status: str
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# -----------------------
# Disputes
# -----------------------
class DisputeOut(BaseModel):
    dispute_id: int = Field(..., alias="dispute_id")
    user_id: int
    listing_id: int
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolution_notes: Optional[str] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ResolveDisputeIn(BaseModel):
    resolved_by: int
    resolution_notes: Optional[str] = None


class ResolveDisputeOut(BaseModel):
    dispute_id: int = Field(..., alias="dispute_id")
    status: str
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
