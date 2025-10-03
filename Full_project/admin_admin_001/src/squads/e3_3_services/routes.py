from fastapi import APIRouter, Depends, Path, Query, status
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.common.database import get_db
from src.common.rbac import admin_required
from .schema import FlaggedBookingOut, AdminActionPayload
from . import service as svc
from src.common.exceptions import not_found

router = APIRouter(prefix="/api/v1/admin/services", tags=["services"])

@router.get("/flagged", response_model=List[FlaggedBookingOut])
def list_flagged(
    status: Optional[str] = Query(None, description="pending|reviewed|resolved"),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    _admin=Depends(admin_required),
):
    items = svc.get_flagged_bookings(db, status=status, date_from=date_from, date_to=date_to)
    return items

@router.post("/providers/{provider_id}/suspend", status_code=status.HTTP_200_OK)
def suspend_provider(
    provider_id: int = Path(..., description="Provider ID"),
    payload: AdminActionPayload = None,
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
):
    # admin contains admin_id stub
    admin_id = payload.admin_id if payload else admin["admin_id"]
    reason = payload.reason if payload else "No reason provided"
    provider, err = svc.suspend_provider(db, provider_id, admin_id, reason)
    if err == "not_found":
        raise not_found("Provider not found")
    return {"provider_id": provider.provider_id, "status": provider.status}

@router.post("/providers/{provider_id}/restore", status_code=status.HTTP_200_OK)
def restore_provider(
    provider_id: int = Path(..., description="Provider ID"),
    payload: AdminActionPayload = None,
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
):
    admin_id = payload.admin_id if payload else admin["admin_id"]
    reason = payload.reason if payload else "No reason provided"
    provider, err = svc.restore_provider(db, provider_id, admin_id, reason)
    if err == "not_found":
        raise not_found("Provider not found")
    return {"provider_id": provider.provider_id, "status": provider.status}
