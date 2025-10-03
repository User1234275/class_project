from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

# --- Import your app's database setup ---
from src.common.database import init_engine, get_engine, Base
from src.models import providers, bookings, flagged_bookings  # import all models

# --- Alembic Config object ---
config = context.config

# --- Logging setup ---
fileConfig(config.config_file_name)

# --- Initialize engine (replace with your actual DB URL) ---
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/admin_all_db"
init_engine(DATABASE_URL)
engine = get_engine()  # engine is now initialized

# --- Metadata for autogenerate ---
target_metadata = Base.metadata

# --- Offline migrations ---
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --- Online migrations ---
def run_migrations_online():
    """Run migrations in 'online' mode using app's engine."""
    connectable = engine
    if connectable is None:
        raise RuntimeError("SQLAlchemy engine is not initialized")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Choose mode ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
