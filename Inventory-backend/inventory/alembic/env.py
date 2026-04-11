from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# 🔹 Alembic Config object
config = context.config

# 🔹 Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔹 Import Base
from app.core.database import Base

# 🔹 IMPORT *ALL* MODELS HERE (VERY IMPORTANT)
from app.models.user import User
from app.models.organization import Organization
from app.models.warehouse import Warehouse
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.stock import StockItem
from app.models.stock_history import StockHistory

# 🔹 Set target metadata for autogenerate
target_metadata = Base.metadata


def get_url():
    """
    Get database URL from environment or fallback
    """
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://inventory_user:inventory_pass@localhost:5432/inventory",
    )


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=get_url(),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# 🔹 Decide offline vs online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
