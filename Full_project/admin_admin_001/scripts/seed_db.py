
import os
from dotenv import load_dotenv
from src.common.database import init_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
init_engine(DATABASE_URL)

from src.common.database import get_session, engine, Base
from src.models import (
    User, UserRole, Marketplace, Dispute, FlaggedListing,
    AdminAction, AuditLog, Provider
)
from sqlalchemy.orm import Session


def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    with next(get_session()) as db:  # type: Session
        # -------------------------
        # Users
        # -------------------------
        admin1 = User(name="Alice Admin", email="alice.admin@example.com", role=UserRole.admin)
        admin2 = User(name="Bob Admin", email="bob.admin@example.com", role=UserRole.admin)

        buyers = [
            User(name="Charlie Buyer", email="charlie.buyer@example.com", role=UserRole.buyer),
            User(name="Diana Buyer", email="diana.buyer@example.com", role=UserRole.buyer),
        ]

        sellers = [
            User(name="Eve Seller", email="eve.seller@example.com", role=UserRole.seller),
            User(name="Frank Seller", email="frank.seller@example.com", role=UserRole.seller),
        ]

        db.add_all([admin1, admin2] + buyers + sellers)
        db.commit()

        # -------------------------
        # Marketplace Listings
        # -------------------------
        listings = [
            Marketplace(user_id=sellers[0].user_id, title="Gaming Laptop"),
            Marketplace(user_id=sellers[0].user_id, title="Wireless Headphones"),
            Marketplace(user_id=sellers[1].user_id, title="Smartphone"),
            Marketplace(user_id=sellers[1].user_id, title="Tablet"),
        ]
        db.add_all(listings)
        db.commit()

        # -------------------------
        # Disputes
        # -------------------------
        disputes = [
            Dispute(listing_id=listings[0].listing_id, raised_by=buyers[0].user_id, status="open"),
            Dispute(listing_id=listings[1].listing_id, raised_by=buyers[1].user_id, status="resolved"),
        ]
        db.add_all(disputes)

        # -------------------------
        # Flagged Listings
        # -------------------------
        flagged = [
            FlaggedListing(listing_id=listings[2].listing_id, reason="Fake product"),
            FlaggedListing(listing_id=listings[3].listing_id, reason="Spam listing"),
        ]
        db.add_all(flagged)

        # -------------------------
        # Providers
        # -------------------------
        providers = [
            Provider(name="UPS", service_type="Shipping"),
            Provider(name="FedEx", service_type="Shipping"),
            Provider(name="Stripe", service_type="Payments"),
        ]
        db.add_all(providers)

        # -------------------------
        # Admin Actions
        # -------------------------
        actions = [
            AdminAction(admin_id=admin1.user_id, action_type="suspend_user", target_id=buyers[0].user_id),
            AdminAction(admin_id=admin2.user_id, action_type="restore_user", target_id=buyers[0].user_id),
            AdminAction(admin_id=admin1.user_id, action_type="remove_listing", target_id=listings[2].listing_id),
        ]
        db.add_all(actions)

        # -------------------------
        # Audit Logs
        # -------------------------
        logs = [
            AuditLog(actor="alice.admin@example.com", action="suspend", resource="user:charlie.buyer@example.com"),
            AuditLog(actor="bob.admin@example.com", action="restore", resource="user:charlie.buyer@example.com"),
            AuditLog(actor="alice.admin@example.com", action="delete", resource="listing:smartphone"),
        ]
        db.add_all(logs)

        db.commit()
        print("✅ Expanded seed data inserted successfully!")


if __name__ == "__main__":
    seed()
