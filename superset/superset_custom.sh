#!/bin/bash

echo "Creating admin user ${ADMIN_USERNAME} email ${ADMIN_EMAIL}"
superset fab create-admin \
    --username "$ADMIN_USERNAME" \
    --firstname Superset \
    --lastname Admin \
    --email "$ADMIN_EMAIL" \
    --password "$ADMIN_PASSWORD"

echo "Upgrading DB"
superset db upgrade

echo "Setup roles"
superset superset init  #setup roles and permissions

echo "Starting server"
/bin/sh -c /usr/bin/run-server.sh