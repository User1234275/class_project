# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv


import os
from dotenv import load_dotenv
from src.common.database import init_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
init_engine(DATABASE_URL)

# Database helpers
from src.common.database import init_engine, get_engine, Base


# Routers (import directly, fail if missing)
from src.squads.e3_1_user_mgmt import routes as user_routes
from src.squads.e3_2_marketplace import routes as marketplace_routes
from src.squads.e3_3_services import routes as services_routes
from src.squads.e3_4_payments import routes as payments_routes
from src.squads.e3_5_analytics import routes as analytics_routes

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Admin Dashboard Service", version="0.1.0")

# CORS (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB engine
init_engine(DATABASE_URL)

@app.on_event("startup")
def startup():
    """Create all tables before first request."""
    try:
        engine = get_engine()
        if engine is None:
            logger.error("DB engine is not initialized.")
            return

        # Import all models to register with SQLAlchemy Base
        try:
            import src.models  # noqa: F401
        except Exception as e:
            logger.warning("Could not import src.models: %s", e)

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/checked successfully.")
    except Exception as exc:
        logger.exception("Error during DB init: %s", exc)

# Always include all routers
app.include_router(user_routes.router, prefix="/api/v1/admin/users", tags=["users"])
app.include_router(marketplace_routes.router, prefix="/api/v1/admin/marketplace", tags=["marketplace"])
app.include_router(services_routes.router, prefix="/api/v1/admin/services", tags=["services"])
app.include_router(payments_routes.router, prefix="/api/v1/admin/payments", tags=["payments"])
app.include_router(analytics_routes.router, prefix="/api/v1/admin/analytics", tags=["analytics"])

# Health endpoints
@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "admin-dashboard-service"}

@app.get("/health", tags=["health"])
def health():
    engine = get_engine()
    db_ok = engine is not None
    return {"status": "ok" if db_ok else "degraded", "database_connected": db_ok}

if __name__ == "__main__":
    for route in app.routes:
        methods = ",".join(route.methods)
        print(f"{methods:10} -> {route.path}")
