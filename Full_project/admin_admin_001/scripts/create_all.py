from src.common.database import Base, engine
from src.models import *

def init_db():
    print("📦 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    init_db()
