#!/bin/bash

# Run the Alembic upgrade command with the database URLs as arguments
alembic upgrade head --x db={$DATABASE_URL}db
