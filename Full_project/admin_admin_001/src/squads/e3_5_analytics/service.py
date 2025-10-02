
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from src.models.audit_logs import AdminDashboardView, AuditLog
from src.models.users import User
from src.models.marketplace import MarketplaceListing
from src.models.disputes import Dispute

def refresh_dashboard(db: Session):
    db.execute(text("REFRESH MATERIALIZED VIEW admin_dashboard_view;"))
    db.commit()
    return db.query(AdminDashboardView).all()









def get_audit_logs(db: Session, skip=0, limit=50, action=None, admin_id=None):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    if admin_id:
        query = query.filter(AuditLog.admin_id == admin_id)
    return query.offset(skip).limit(limit).all()




def user_summary(db: Session):
    return {
        "total": db.query(func.count(User.id)).scalar(),
        "active": db.query(func.count(User.id)).filter(User.status == "active").scalar(),
        "suspended": db.query(func.count(User.id)).filter(User.status == "suspended").scalar(),
    }



def marketplace_summary(db: Session):
    return {
        "total": db.query(func.count(MarketplaceListing.id)).scalar(),
        "active": db.query(func.count(MarketplaceListing.id)).filter(MarketplaceListing.status == "active").scalar(),
        "pending": db.query(func.count(MarketplaceListing.id)).filter(MarketplaceListing.status == "pending").scalar(),
    }



def dispute_summary(db: Session):
    return {
        "total": db.query(func.count(Dispute.id)).scalar(),
        "open": db.query(func.count(Dispute.id)).filter(Dispute.status == "open").scalar(),
        "resolved": db.query(func.count(Dispute.id)).filter(Dispute.status == "resolved").scalar(),
    }
