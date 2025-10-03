# from sqlalchemy.orm import Session
# from src.models.providers import Provider
# from src.models.flagged_bookings import FlaggedBooking
# from src.models.admin_action import AdminAction
# from src.common.events import publish_event
# from datetime import datetime




# def suspend_provider(db: Session, provider_id: int, admin_id: int, reason: str):
#     provider = db.query(Provider).filter(Provider.provider_id == provider_id).one_or_none()
#     if not provider:
#         return None, "not_found"
#     # idempotent: if already suspended, still return current state
#     if provider.status != "suspended":
#         provider.status = "suspended"
#         provider.updated_at = datetime.utcnow()
#         db.add(provider)
#         db.flush()
#     # log action (immutable)
#     db.query(FlaggedBooking).filter(
#         FlaggedBooking.provider_id == provider_id
#     ).update({"status": "provider_suspended"})

#     action = AdminAction(admin_id=admin_id, action_type="suspend", target_id=provider_id)
#     db.add(action)
#     db.commit()
#     publish_event("admin.action.logged", {"admin_id": admin_id, "provider_id": provider_id, "action": "suspend", "reason": reason})
#     return provider, None

# def restore_provider(db: Session, provider_id: int, admin_id: int, reason: str):
#     provider = db.query(Provider).filter(Provider.provider_id == provider_id).one_or_none()
#     if not provider:
#         return None, "not_found"
#     if provider.status != "active":
#         provider.status = "active"
#         provider.updated_at = datetime.utcnow()
#         db.add(provider)
#         db.flush()
#     action = AdminAction(admin_id=admin_id, action_type="restore", target_id=provider_id)
#     db.add(action)
#     db.commit()
#     publish_event("admin.action.logged", {"admin_id": admin_id, "provider_id": provider_id, "action": "restore", "reason": reason})
#     return provider, None

# def get_flagged_bookings(db: Session, status: str = None, date_from=None, date_to=None):
#     from src.models.flagged_bookings import FlaggedBooking
#     q = db.query(FlaggedBooking)
#     if status:
#         q = q.filter(FlaggedBooking.status == status)
#     if date_from:
#         q = q.filter(FlaggedBooking.created_at >= date_from)
#     if date_to:
#         q = q.filter(FlaggedBooking.created_at <= date_to)
#     return q.order_by(FlaggedBooking.created_at.desc()).all()



from sqlalchemy.orm import Session
from src.models.providers import Provider
from src.models.flagged_bookings import FlaggedBooking
from src.models.admin_action import AdminAction
from src.common.events import publish_event
from datetime import datetime


def suspend_provider(db: Session, provider_id: int, admin_id: int, reason: str):
    provider = db.query(Provider).filter(Provider.provider_id == provider_id).one_or_none()
    if not provider:
        return None, "not_found"

    # Idempotent: if already suspended, still return current state
    if provider.status != "suspended":
        provider.status = "suspended"
        provider.updated_at = datetime.utcnow()
        db.add(provider)
        db.flush()

        # Update all flagged bookings for this provider
        db.query(FlaggedBooking).filter(
            FlaggedBooking.provider_id == provider_id
        ).update({"status": "provider_suspended"}, synchronize_session=False)

    # Log admin action
    action = AdminAction(admin_id=admin_id, action_type="suspend", target_id=provider_id, reason=reason)
    db.add(action)
    db.commit()

    # Publish event
    publish_event("admin.action.logged", {
        "admin_id": admin_id,
        "provider_id": provider_id,
        "action": "suspend",
        "reason": reason
    })

    return provider, None


def restore_provider(db: Session, provider_id: int, admin_id: int, reason: str):
    provider = db.query(Provider).filter(Provider.provider_id == provider_id).one_or_none()
    if not provider:
        return None, "not_found"

    if provider.status != "active":
        provider.status = "active"
        provider.updated_at = datetime.utcnow()
        db.add(provider)
        db.flush()

        # Update all flagged bookings for this provider
        db.query(FlaggedBooking).filter(
            FlaggedBooking.provider_id == provider_id
        ).update({"status": "resolved"}, synchronize_session=False)

    # Log admin action
    action = AdminAction(admin_id=admin_id, action_type="restore", target_id=provider_id, reason=reason)
    db.add(action)
    db.commit()

    # Publish event
    publish_event("admin.action.logged", {
        "admin_id": admin_id,
        "provider_id": provider_id,
        "action": "restore",
        "reason": reason
    })

    return provider, None





def get_flagged_bookings(db: Session, status: str = None, date_from=None, date_to=None):
    q = db.query(FlaggedBooking)
    if status:
        q = q.filter(FlaggedBooking.status == status)
    if date_from:
        q = q.filter(FlaggedBooking.created_at >= date_from)
    if date_to:
        q = q.filter(FlaggedBooking.created_at <= date_to)
    return q.order_by(FlaggedBooking.created_at.desc()).all()
