import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import Base  # noqa: E402
from settings import APP_ENV, DATABASE_URL  # noqa: E402


def run_migrations_online():
    connectable = context.config.attributes.get("connection")

    # For app database
    if connectable is None:
        if APP_ENV == "dev":
            db_url = "postgresql://admin:admin@127.0.0.1:5432/db"
        else:
            db_url = DATABASE_URL
        connectable = engine_from_config(
            context.config.get_section(context.config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            url=db_url,
        )
        # Run migrations for app database
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=Base)
            with context.begin_transaction():
                context.run_migrations()


def run_migrations_offline():
    context.configure(url=DATABASE_URL)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


run_migrations()
