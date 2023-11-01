#!/bin/bash

# Run the Alembic upgrade command with the database URLs as arguments
alembic upgrade head --x app_db=$APP_DB_URL --x client_db=$CLIENT_DB_URL
