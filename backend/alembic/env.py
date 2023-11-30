from alembic import context
from sqlalchemy import engine_from_config, pool

from models.app.base import Base as app_db_target_metadata
from models.client.base import Base as client_db_target_metadata 


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
                    target_metadata=app_db_target_metadata
                )
                with context.begin_transaction():
                    context.run_migrations()

    # For client database
    db_url_db2 = context.get_x_argument(as_dictionary=True).get('client_db', None)
    if db_url_db2:
        connectable_db2 = engine_from_config(
            context.config.get_section(context.config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            url=db_url_db2,
        )
        # Run migrations for client database
        with connectable_db2.connect() as connection_db2:
            context.configure(
                connection=connection_db2,
                target_metadata=client_db_target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()
