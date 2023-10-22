#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE app_db;
    CREATE DATABASE client_db;
    CREATE DATABASE superset;
    CREATE USER app_user WITH PASSWORD 'app_password';
    CREATE USER client_user WITH PASSWORD 'client_password';
    CREATE USER superset_user WITH PASSWORD 'superset_password';
    GRANT ALL PRIVILEGES ON DATABASE app_db TO app_user;
    GRANT ALL PRIVILEGES ON DATABASE client_db TO client_user;
    GRANT ALL PRIVILEGES ON DATABASE superset TO superset_user;
EOSQL
