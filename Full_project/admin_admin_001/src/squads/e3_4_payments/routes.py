
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from uuid import UUID
from src.models.admin_flags import FlagStatus
from src.common.database import get_db
from src.squads.e3_4_payments import service, schema

router = APIRouter(prefix="/api/v1/admin/payments", tags=["payments"])






@router.get("/flagged", response_model=list[schema.FlaggedTransactionResponse])
def get_flagged(
    status_filter: Optional[FlagStatus] = Query(default=None, description="Filter by status"),
    db: Session = Depends(get_db),
):
    flagged = service.get_flagged_transactions(db, status_filter)
    if not flagged:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No flagged transactions"
        )
    return flagged


@router.get("/disputes", response_model=list[schema.DisputeResponse])
def get_disputes(db: Session = Depends(get_db)):
    disputes = service.get_all_disputes(db)
    if not disputes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No disputes found"
        )
    return disputes


@router.post("/disputes/{dispute_id}/resolve", response_model=schema.DisputeResponse)
def resolve_dispute(
    dispute_id: UUID,
    body: schema.DisputeResolveRequest,
    db: Session = Depends(get_db)
):
    dispute = service.resolve_dispute(db, dispute_id, body)
    if not dispute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispute not found"
        )
    return dispute



@router.post("/flagged/{flagged_id}/resolve", response_model=schema.FlaggedTransactionResponse)
def resolve_flagged_transaction(
    flagged_id: UUID,
    body: schema.FlaggedResolveRequest,
    db: Session = Depends(get_db)
):
    flagged = service.resolve_flagged_transaction(db, flagged_id, body)
    if not flagged:
        raise HTTPException(status_code=404, detail="Flagged transaction not found")
    return flagged

