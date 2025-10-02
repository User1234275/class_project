from sqlalchemy.orm import Session
from src.models.users import User
from src.models.admin_action import AdminAction
from src.common.exceptions import not_found, conflict
from typing import Optional
from datetime import datetime
from src.common.logger import logger

def list_users(db: Session, name: Optional[str]=None, email: Optional[str]=None, status: Optional[str]=None, role: Optional[str]=None, page: int=1, limit: int=25):
    q = db.query(User)
    if name:
        q = q.filter(User.name.ilike(f"%{name}%"))
    if email:
        q = q.filter(User.email.ilike(f"%{email}%"))
    if status:
        q = q.filter(User.status == status)
    if role:
        q = q.filter(User.role == role)  # <-- add this line
    total = q.count()
    q = q.order_by(User.user_id).offset((page-1)*limit).limit(limit)
    users = q.all()
    meta = {"page": page, "limit": limit, "total": total, "pages": (total + limit - 1)//limit}
    return users, meta

def suspend_user(db: Session, user_id: int, admin_id: int, reason: Optional[str]=None):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise not_found("User not found")
    if user.status == "suspended":
        raise conflict("User already suspended")
    user.status = "suspended"
    user.updated_at = datetime.utcnow()
    db.add(user)
    log = AdminAction(admin_id=admin_id, action_type="suspend", target_id=user_id, reason=reason)
    db.add(log)
    db.commit()
    db.refresh(user)
    logger.info("Admin %s suspended user %s", admin_id, user_id)
    return user

def restore_user(db: Session, user_id: int, admin_id: int, reason: Optional[str]=None):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise not_found("User not found")
    if user.status == "active":
        raise conflict("User already active")
    user.status = "active"
    user.updated_at = datetime.utcnow()
    db.add(user)
    log = AdminAction(admin_id=admin_id, action_type="restore", target_id=user_id, reason=reason)
    db.add(log)
    db.commit()
    db.refresh(user)
    logger.info("Admin %s restored user %s", admin_id, user_id)
    return user
