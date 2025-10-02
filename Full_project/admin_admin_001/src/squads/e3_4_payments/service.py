from sqlalchemy.orm import Session
from src.models.admin_flags import FlaggedTransaction, FlagStatus
from src.models.disputes import PaymentDispute, DisputeStatus
from src.models.audit_logs import AuditLog, ActionType
from src.squads.e3_4_payments.schema import DisputeResolveRequest
from datetime import datetime
import uuid


def get_flagged_transactions(db: Session):
    return db.query(FlaggedTransaction).filter(FlaggedTransaction.status == FlagStatus.pending).all()


def resolve_dispute(db: Session, dispute_id: uuid.UUID, body: DisputeResolveRequest):
    dispute = db.query(PaymentDispute).filter(PaymentDispute.id == dispute_id).first()
    if not dispute:
        return None

    if dispute.status == DisputeStatus.resolved:
        raise ValueError("DISPUTE_ALREADY_RESOLVED")

    dispute.status = DisputeStatus.resolved
    dispute.resolved_at = datetime.utcnow()

    audit = AuditLog(
        admin_id=body.resolved_by,
        action_type=ActionType.dispute_resolved,
        target_id=dispute.id,
        metadata={"resolution": body.resolution},
    )
    db.add(audit)
    db.commit()
    db.refresh(dispute)

    return dispute


def get_all_disputes(db: Session):
    return db.query(PaymentDispute).all()



def resolve_flagged_transaction(db: Session, flagged_id: uuid.UUID, body):
    flagged = db.query(FlaggedTransaction).filter(FlaggedTransaction.id == flagged_id).first()
    if not flagged:
        return None

    flagged.status = body.status

    audit = AuditLog(
        admin_id=body.resolved_by,
        action_type=ActionType.dispute_resolved,
        target_id=flagged.id,
        extra_metadata={"note": body.note or "Flagged txn reviewed"}
    )
    db.add(audit)
    db.commit()
    db.refresh(flagged)
    return flagged


from typing import Optional


def get_flagged_transactions(db: Session, status: Optional[FlagStatus] = None):
    query = db.query(FlaggedTransaction)
    if status:
        query = query.filter(FlaggedTransaction.status == status)
    return query.all()

