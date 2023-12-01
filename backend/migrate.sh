#!/bin/bash

# Run the Alembic upgrade command with the database URLs as arguments
alembic upgrade head --x db={$DB_URL}db
