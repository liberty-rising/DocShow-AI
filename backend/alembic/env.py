from alembic import context
from sqlalchemy import engine_from_config, pool

from models.base import Base


def run_migrations_online():
    connectable = context.config.attributes.get('connection')

    # For app database
    if connectable is None:
        db_url = context.get_x_argument(as_dictionary=True).get('app_db', None)
        if db_url:
            connectable = engine_from_config(
                context.config.get_section(context.config.config_ini_section),
                prefix='sqlalchemy.',
                poolclass=pool.NullPool,
                url=db_url,
            )
            # Run migrations for app database
            with connectable.connect() as connection:
                context.configure(
                    connection=connection,
                    target_metadata=Base
                )
                with context.begin_transaction():
                    context.run_migrations()