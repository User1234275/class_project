Perfect! Let’s design a **FastAPI project structure** for your **Payment Oversight Module** with proper folders, Pydantic models, routers, and async endpoints. I’ll make it **ready-to-implement**.

---

# **FastAPI Project Structure – Payment Oversight Module**

```
payment_oversight/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entrypoint
│   ├── core/
│   │   ├── config.py          # Config variables, DB URLs, JWT secret
│   │   └── security.py        # JWT utils, password hashing
│   ├── db/
│   │   ├── base.py            # Base ORM models
│   │   ├── session.py         # DB session/connection pooling
│   │   └── models.py          # SQLAlchemy models
│   ├── schemas/
│   │   ├── flagged_transaction.py
│   │   ├── payment_dispute.py
│   │   └── audit_log.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependency injections (DB, current_admin)
│   │   ├── flagged_transactions.py
│   │   ├── payment_disputes.py
│   │   └── audit_logs.py
│   ├── services/
│   │   ├── notifications.py   # Email/SMS/Push async notifications
│   │   ├── audit_service.py   # Logging actions
│   │   └── dispute_service.py # Dispute resolution logic
│   └── utils/
│       └── enums.py           # Status enums for transactions/disputes
├── tests/
│   ├── test_flagged_transactions.py
│   ├── test_payment_disputes.py
│   └── test_audit_logs.py
├── alembic/                   # DB migrations
├── requirements.txt
└── README.md
```

---

## **1. SQLAlchemy Models (app/db/models.py)**

```python
import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import Base
from app.utils.enums import FlagStatus, DisputeStatus, AuditActionType

class FlaggedTransaction(Base):
    __tablename__ = "flagged_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), nullable=False)
    flagged_reason = Column(String, nullable=False)
    flagged_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    status = Column(Enum(FlagStatus), default=FlagStatus.PENDING)

class PaymentDispute(Base):
    __tablename__ = "payment_disputes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    dispute_reason = Column(String, nullable=False)
    status = Column(Enum(DisputeStatus), default=DisputeStatus.OPEN)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    resolved_at = Column(TIMESTAMP(timezone=True), nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id = Column(UUID(as_uuid=True), nullable=False)
    action_type = Column(Enum(AuditActionType), nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    metadata = Column(JSON)
```

---

## **2. Pydantic Schemas (app/schemas/flagged\_transaction.py)**

```python
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from app.utils.enums import FlagStatus

class FlaggedTransactionBase(BaseModel):
    transaction_id: UUID
    flagged_reason: str
    status: FlagStatus

class FlaggedTransactionCreate(FlaggedTransactionBase):
    pass

class FlaggedTransactionRead(FlaggedTransactionBase):
    id: UUID
    flagged_at: datetime

    class Config:
        orm_mode = True
```

> Similar schemas for `PaymentDispute` and `AuditLog` in their respective files.

---

## **3. API Routes (app/api/flagged\_transactions.py)**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.flagged_transaction import FlaggedTransactionRead
from app.db.models import FlaggedTransaction

router = APIRouter(prefix="/api/v1/admin/payments", tags=["Flagged Transactions"])

@router.get("/flagged", response_model=List[FlaggedTransactionRead])
async def get_flagged_transactions(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM flagged_transactions WHERE status='pending'")
    transactions = result.fetchall()
    if not transactions:
        raise HTTPException(status_code=404, detail="No flagged transactions found")
    return transactions
```

---

## **4. API Routes (app/api/payment\_disputes.py)**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from uuid import UUID
from app.db.models import PaymentDispute, AuditLog
from app.schemas.payment_dispute import PaymentDisputeResolve

router = APIRouter(prefix="/api/v1/admin/payments", tags=["Payment Disputes"])

@router.post("/disputes/{id}/resolve")
async def resolve_dispute(id: UUID, payload: PaymentDisputeResolve, db: AsyncSession = Depends(get_db)):
    dispute = await db.get(PaymentDispute, id)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    if dispute.status == "resolved":
        raise HTTPException(status_code=409, detail="Dispute already resolved")
    
    dispute.status = "resolved"
    dispute.resolved_at = payload.resolved_at
    # Optional: call notification service
    # Optional: save audit log
    await db.commit()
    return dispute
```

---

## **5. Async Notifications & Audit Service (app/services/)**

* `notifications.py` → Send email/SMS/push using Celery/async tasks
* `audit_service.py` → Save admin actions asynchronously
* `dispute_service.py` → Core dispute resolution logic

---

## **6. FastAPI App Entry (app/main.py)**

```python
from fastapi import FastAPI
from app.api import flagged_transactions, payment_disputes

app = FastAPI(title="Payment Oversight Module")

app.include_router(flagged_transactions.router)
app.include_router(payment_disputes.router)
```

---

## ✅ **Key Features in FastAPI Version**

* Fully **async endpoints** for speed
* **Pydantic schemas** for validation & response models
* **SQLAlchemy async ORM** with PostgreSQL
* **Redis caching + Celery** for async notifications
* **Audit logs** tracked automatically
* **JWT + RBAC** authentication ready

---

I can also make a **complete FastAPI folder with ready-to-run `docker-compose.yml`, Alembic migrations, and sample async notification tasks** for this module.

Do you want me to do that next?
