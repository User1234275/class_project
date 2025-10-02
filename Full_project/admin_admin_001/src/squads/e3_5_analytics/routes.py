
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from src.common.database import get_db
from . import schema, service
from src.models.analytics import AnalyticsView 


router = APIRouter(prefix="/api/admin/analytics", tags=["Analytics"])




@router.get("/", response_model=list[dict])
def dashboard_metrics(db: Session = Depends(get_db)):
    try:
        # Query the admin_dashboard_view table/view directly
        metrics = db.query(AnalyticsView).all()

        # Convert SQLAlchemy objects to dicts
        result = [
            {
                "id": m.id,
                "metric_name": m.metric_name,
                "metric_value": m.metric_value,
                "time_bucket": m.time_bucket
            }
            for m in metrics
        ]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard", response_model=List[schema.DashboardMetric])
def dashboard_metrics(db: Session = Depends(get_db)):
    return service.refresh_dashboard(db)





@router.get("/logs", response_model=List[schema.AuditLogOut])
def list_audit_logs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    action: Optional[str] = Query(None),
    admin_id: Optional[int] = Query(None),
):
    return service.get_audit_logs(db, skip, limit, action, admin_id)




@router.get("/users", response_model=schema.UserActivitySummary)
def user_activity_summary(db: Session = Depends(get_db)):
    stats = service.user_summary(db)
    return schema.UserActivitySummary(
        total_users=stats["total"], active_users=stats["active"], suspended_users=stats["suspended"]
    )






@router.get("/marketplace", response_model=schema.MarketplaceStats)
def marketplace_stats(db: Session = Depends(get_db)):
    stats = service.marketplace_summary(db)
    return schema.MarketplaceStats(
        total_listings=stats["total"], active_listings=stats["active"], pending_listings=stats["pending"]
    )





@router.get("/disputes", response_model=schema.DisputeSummary)
def dispute_summary(db: Session = Depends(get_db)):
    stats = service.dispute_summary(db)
    return schema.DisputeSummary(
        total_disputes=stats["total"], open_disputes=stats["open"], resolved_disputes=stats["resolved"]
    )
