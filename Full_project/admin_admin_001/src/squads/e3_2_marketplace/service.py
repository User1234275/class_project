from sqlalchemy.orm import Session
from src.models.flagged_listings import FlaggedListing
from src.models.disputes import Dispute
from src.models.audit_logs import AuditLog
from src.common.events import publish_event
from src.common.exceptions import not_found, conflict
import json

def list_flagged(session: Session, status: str = None):
    q = session.query(FlaggedListing)
    if status:
        q = q.filter(FlaggedListing.status == status)
    return q.order_by(FlaggedListing.created_at.desc()).all()

def resolve_flag(session: Session, flag_id: int, resolved_by: int, notes: str = None):
    flag = session.query(FlaggedListing).filter(FlaggedListing.flag_id == flag_id).first()
    if not flag:
        raise not_found(detail=f"Flag id {flag_id} not found")
    if flag.status == "resolved":
        raise conflict(detail=f"Flag id {flag_id} already resolved")

    flag.status = "resolved"
    flag.resolved_at = func_now()
    flag.resolved_by = resolved_by
    session.add(flag)

    # Write audit log
    details_dict = {"notes": notes}
    a = AuditLog(
        actor=str(resolved_by),  # Use admin id as actor
        action="resolve_flagged_listing",
        resource="flagged_listing",
        entity_type="flagged_listing",
        entity_id=flag_id,
        details=json.dumps(details_dict)
    )
    session.add(a)
    session.commit()

    publish_event("admin.action.logged", {
        "admin_id": resolved_by,
        "action": "resolve_flagged_listing",
        "entity_type": "flagged_listing",
        "entity_id": flag_id,
    })

    return flag

def resolve_dispute(session: Session, dispute_id: int, resolved_by: int, resolution_notes: str = None):
    dispute = session.query(Dispute).filter(Dispute.dispute_id == dispute_id).first()
    if not dispute:
        raise not_found(detail=f"Dispute id {dispute_id} not found")
    if dispute.status == "resolved":
        raise conflict(detail=f"Dispute id {dispute_id} already resolved")

    dispute.status = "resolved"
    dispute.resolved_at = func_now()
    dispute.resolved_by = resolved_by
    dispute.resolution_notes = resolution_notes
    session.add(dispute)

    # audit log
    a = AuditLog(
        admin_id=resolved_by,
        actor=str(resolved_by),  # Use admin id as actor
        action="resolve_dispute",
        resource="dispute",
        entity_type="dispute",
        entity_id=dispute_id,
        details=json.dumps({"resolution_notes": resolution_notes})
    )
    session.add(a)
    session.commit()

    # publish event & (optionally) notifications
    publish_event("admin.action.logged", {
        "admin_id": resolved_by,
        "action": "resolve_dispute",
        "entity_type": "dispute",
        "entity_id": dispute_id,
        "resolution_notes": resolution_notes
    })

    # placeholder: notificationService.sendDisputeResolution(...)
    return dispute
    
def create_flagged_listing(session: Session, listing_id: int, reason: str, status: str = "pending"):
    new_flag = FlaggedListing(
        listing_id=listing_id,
        reason=reason,
        status=status
        # flagged_at and created_at will be set automatically
    )
    session.add(new_flag)
    session.commit()
    session.refresh(new_flag)
    return new_flag

# small helper to get current timestamp (SQL-friendly)
from datetime import datetime
def func_now():
    return datetime.utcnow()





# from sqlalchemy.orm import Session
# from src.models.flagged_listings import FlaggedListing
# from src.models.disputes import Dispute
# from src.models.audit_logs import AuditLog
# from src.common.events import publish_event
# from src.common.exceptions import not_found, conflict
# from datetime import datetime
# import json

# # small helper to get current timestamp (SQL-friendly)
# def func_now():
#     return datetime.utcnow()


# def list_flagged(session: Session, status: str = None):
#     q = session.query(FlaggedListing)
#     if status:
#         q = q.filter(FlaggedListing.status == status)
#     return q.order_by(FlaggedListing.created_at.desc()).all()


# def resolve_flag(session: Session, flag_id: int, resolved_by: int, notes: str = None):
#     flag = session.query(FlaggedListing).filter(FlaggedListing.flag_id == flag_id).first()
#     if not flag:
#         raise not_found(detail=f"Flag id {flag_id} not found")
#     if flag.status == "resolved":
#         raise conflict(detail=f"Flag id {flag_id} already resolved")

#     flag.status = "resolved"
#     flag.resolved_at = func_now()
#     flag.resolved_by = resolved_by
#     session.add(flag)

#     # Write audit log
#     details_dict = {"notes": notes}
#     a = AuditLog(
#         actor=str(resolved_by),  # Use admin id as actor
#         action="resolve_flagged_listing",
#         resource="flagged_listing",
#         entity_type="flagged_listing",
#         entity_id=flag_id,
#         details=json.dumps(details_dict)
#     )
#     session.add(a)
#     session.commit()
#     session.refresh(flag)

#     publish_event("admin.action.logged", {
#         "admin_id": resolved_by,
#         "action": "resolve_flagged_listing",
#         "entity_type": "flagged_listing",
#         "entity_id": flag_id,
#     })

#     # ✅ Return dict that matches ResolveFlagOut
#     return {
#         "id": flag.flag_id,  # note: FlaggedListing model uses flag_id PK
#         "status": flag.status,
#         "resolved_at": flag.resolved_at,
#         "resolved_by": flag.resolved_by,
#     }


# def resolve_dispute(session: Session, dispute_id: int, resolved_by: int, resolution_notes: str = None):
#     # dispute = session.query(Dispute).filter(Dispute.id == dispute_id).first()
#     dispute = session.query(Dispute).filter(Dispute.dispute_id == dispute_id).first()

#     if not dispute:
#         raise not_found(detail=f"Dispute id {dispute_id} not found")
#     if dispute.status == "resolved":
#         raise conflict(detail=f"Dispute id {dispute_id} already resolved")

#     dispute.status = "resolved"
#     dispute.resolved_at = func_now()
#     dispute.resolved_by = resolved_by
#     dispute.resolution_notes = resolution_notes
#     session.add(dispute)

#     # audit log
#     a = AuditLog(
#         admin_id=resolved_by,
#         actor=str(resolved_by),  # Use admin id as actor
#         action="resolve_dispute",
#         entity_type="dispute",
#         entity_id=dispute_id,
#         details=json.dumps({"resolution_notes": resolution_notes})
#     )
#     session.add(a)
#     session.commit()
#     session.refresh(dispute)

#     publish_event("admin.action.logged", {
#         "admin_id": resolved_by,
#         "action": "resolve_dispute",
#         "entity_type": "dispute",
#         "entity_id": dispute_id,
#         "resolution_notes": resolution_notes
#     })

#     # ✅ Return dict that matches ResolveDisputeOut
#     return {
#         "id": dispute.dispute_id,
#         "status": dispute.status,
#         "resolved_at": dispute.resolved_at,
#         "resolved_by": dispute.resolved_by,
#     }



# def create_flagged_listing(session: Session, listing_id: int, reason: str, status: str = "pending"):
#     new_flag = FlaggedListing(
#         listing_id=listing_id,
#         reason=reason,
#         status=status
#         # flagged_at and created_at will be set automatically
#     )
#     session.add(new_flag)
#     session.commit()
#     session.refresh(new_flag)

#     # ✅ Return dict that matches FlaggedListingOut
#     return {
#         "id": new_flag.flag_id,   # matches FlaggedListingOut.id (aliased to flag_id)
#         "listing_id": new_flag.listing_id,
#         "reason": new_flag.reason,
#         "status": new_flag.status,
#         "created_at": new_flag.created_at,
#         "resolved_at": new_flag.resolved_at,
#         "resolved_by": new_flag.resolved_by,
#     }


# from sqlalchemy.orm import Session
# from src.models.flagged_listings import FlaggedListing
# from src.models.disputes import Dispute
# from src.models.audit_logs import AuditLog
# from src.common.events import publish_event
# from src.common.exceptions import not_found, conflict
# from datetime import datetime
# import json

# # -----------------------
# # Helper
# # -----------------------
# def func_now():
#     """Return current UTC timestamp for DB"""
#     return datetime.utcnow()

# # -----------------------
# # Flagged Listings
# # -----------------------
# def list_flagged(session: Session, status: str = None):
#     """List all flagged listings, optionally filtered by status"""
#     q = session.query(FlaggedListing)
#     if status:
#         q = q.filter(FlaggedListing.status == status)
#     flagged_list = q.order_by(FlaggedListing.created_at.desc()).all()

#     # Convert ORM objects to dicts matching FlaggedListingOut
#     result = []
#     for f in flagged_list:
#         result.append({
#             "id": f.flag_id,
#             "listing_id": f.listing_id,
#             "reason": f.reason,
#             "status": f.status,
#             "created_at": f.created_at,
#             "resolved_at": f.resolved_at,
#             "resolved_by": f.resolved_by,
#         })
#     return result

# def resolve_flag(session: Session, flag_id: int, resolved_by: int, notes: str = None):
#     """Resolve a flagged listing"""
#     flag = session.query(FlaggedListing).filter(FlaggedListing.flag_id == flag_id).first()
#     if not flag:
#         raise not_found(detail=f"Flag id {flag_id} not found")
#     if flag.status == "resolved":
#         raise conflict(detail=f"Flag id {flag_id} already resolved")

#     flag.status = "resolved"
#     flag.resolved_at = func_now()
#     flag.resolved_by = resolved_by
#     session.add(flag)

#     # Audit log
#     details_dict = {"notes": notes}
#     a = AuditLog(
#         actor=str(resolved_by),
#         action="resolve_flagged_listing",
#         resource="flagged_listing",
#         entity_type="flagged_listing",
#         entity_id=flag_id,
#         details=json.dumps(details_dict)
#     )
#     session.add(a)
#     session.commit()
#     session.refresh(flag)

#     publish_event("admin.action.logged", {
#         "admin_id": resolved_by,
#         "action": "resolve_flagged_listing",
#         "entity_type": "flagged_listing",
#         "entity_id": flag_id,
#     })

#     return {
#         "id": flag.flag_id,
#         "status": flag.status,
#         "resolved_at": flag.resolved_at,
#         "resolved_by": flag.resolved_by,
#     }

# def create_flagged_listing(session: Session, listing_id: int, reason: str, status: str = "pending"):
#     """Create a new flagged listing"""
#     new_flag = FlaggedListing(
#         listing_id=listing_id,
#         reason=reason,
#         status=status
#     )
#     session.add(new_flag)
#     session.commit()
#     session.refresh(new_flag)

#     return {
#         "id": new_flag.flag_id,
#         "listing_id": new_flag.listing_id,
#         "reason": new_flag.reason,
#         "status": new_flag.status,
#         "created_at": new_flag.created_at,
#         "resolved_at": new_flag.resolved_at,
#         "resolved_by": new_flag.resolved_by,
#     }

# # -----------------------
# # Disputes
# # -----------------------
# def list_disputes(session: Session, status: str = None):
#     """List all disputes, optionally filtered by status"""
#     q = session.query(Dispute)
#     if status:
#         q = q.filter(Dispute.status == status)
#     disputes = q.order_by(Dispute.created_at.desc()).all()

#     # Convert ORM objects to dicts matching DisputeOut
#     result = []
#     for d in disputes:
#         result.append({
#             "id": d.dispute_id,
#             "user_id": d.user_id,
#             "listing_id": d.listing_id,
#             "status": d.status,
#             "created_at": d.created_at,
#             "resolved_at": d.resolved_at,
#             "resolved_by": d.resolved_by,
#             "resolution_notes": d.resolution_notes,
#         })
#     return result

# def resolve_dispute(session: Session, dispute_id: int, resolved_by: int, resolution_notes: str = None):
#     """Resolve a dispute"""
#     dispute = session.query(Dispute).filter(Dispute.dispute_id == dispute_id).first()
#     if not dispute:
#         raise not_found(detail=f"Dispute id {dispute_id} not found")
#     if dispute.status == "resolved":
#         raise conflict(detail=f"Dispute id {dispute_id} already resolved")

#     dispute.status = "resolved"
#     dispute.resolved_at = func_now()
#     dispute.resolved_by = resolved_by
#     dispute.resolution_notes = resolution_notes
#     session.add(dispute)

#     # Audit log
#     a = AuditLog(
#         admin_id=resolved_by,
#         actor=str(resolved_by),
#         action="resolve_dispute",
#         entity_type="dispute",
#         entity_id=dispute_id,
#         details=json.dumps({"resolution_notes": resolution_notes})
#     )
#     session.add(a)
#     session.commit()
#     session.refresh(dispute)

#     publish_event("admin.action.logged", {
#         "admin_id": resolved_by,
#         "action": "resolve_dispute",
#         "entity_type": "dispute",
#         "entity_id": dispute_id,
#         "resolution_notes": resolution_notes
#     })

#     return {
#         "id": dispute.dispute_id,
#         "status": dispute.status,
#         "resolved_at": dispute.resolved_at,
#         "resolved_by": dispute.resolved_by,
#     }
