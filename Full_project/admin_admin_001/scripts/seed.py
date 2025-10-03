import os
from dotenv import load_dotenv
from src.common.database import init_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
init_engine(DATABASE_URL)


from sqlalchemy.orm import Session
from src.common.database import SessionLocal, Base, engine
from src.models.providers import Provider
from src.models.bookings import Booking
from src.models.flagged_bookings import FlaggedBooking, FlagStatus

def seed():
    # Create all tables if not already created
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    # --- Providers ---
    provider1 = Provider(name="Alice's Plumbing", service_type="plumbing")
    provider2 = Provider(name="Bob's Cleaning", service_type="cleaning")

    db.add_all([provider1, provider2])
    db.commit()

    # Refresh to get IDs
    db.refresh(provider1)
    db.refresh(provider2)

    # --- Bookings ---
    booking1 = Booking(user_id=1, provider_id=provider1.provider_id, service_details="Pipe repair")
    booking2 = Booking(user_id=2, provider_id=provider2.provider_id, service_details="House cleaning")
    booking3 = Booking(user_id=3, provider_id=provider1.provider_id, service_details="Drain unclogging")

    db.add_all([booking1, booking2, booking3])
    db.commit()

    db.refresh(booking1)
    db.refresh(booking2)
    db.refresh(booking3)

    # --- Flagged Bookings ---
    flagged1 = FlaggedBooking(
        booking_id=booking1.booking_id,
        provider_id=provider1.provider_id,
        reason="Customer complaint: Overcharged",
        status=FlagStatus.pending,
    )
    flagged2 = FlaggedBooking(
        booking_id=booking2.booking_id,
        provider_id=provider2.provider_id,
        reason="Service not delivered",
        status=FlagStatus.reviewed,
    )

    db.add_all([flagged1, flagged2])
    db.commit()
    db.close()
    print("✅ Database seeded successfully")

if __name__ == "__main__":
    seed()
