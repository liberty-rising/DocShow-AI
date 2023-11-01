#!/bin/bash
# wait-for.sh
#
# This script is used to wait for Postgres and Superset services to become available
# before executing a specified command. This is useful in docker-compose setups
# where services depend on each other to be fully initialized before starting.
#
# Usage:
#   ./wait-for.sh [HOST] [PORT] -- [COMMAND]
#
# Arguments:
#   HOST: The hostname of the Postgres server.
#   PORT: The port number of the Postgres server.
#   COMMAND: The command to execute once Postgres and Superset are available.
#
# Functions:
#   - wait_for_postgres: Continuously checks the availability of the Postgres server
#                        using the psql command, and sleeps for 1 second between checks.
#   - wait_for_superset: Continuously checks the availability of the Superset service
#                        using the curl command, and sleeps for 1 second between checks.
#
# Environment Variables:
#   - POSTGRES_USER: The username to use for connecting to Postgres.
#   - POSTGRES_PASSWORD: The password to use for connecting to Postgres.

set -e

host="$1"
port="$2"
shift
shift
cmd="$@"

wait_for_postgres() {

  until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "$POSTGRES_USER" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
  done

  >&2 echo "Postgres is up - executing command"
}

wait_for_superset() {
  until curl -sfL "http://superset:8088/health"; do
    >&2 echo "Superset is unavailable - sleeping"
    sleep 1
  done

  >&2 echo "Superset is up"
}

wait_for_postgres
wait_for_superset
exec $cmd
