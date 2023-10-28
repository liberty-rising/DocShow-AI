#!/bin/bash
# wait-for.sh

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
