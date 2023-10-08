# Navigate to the /backend directory
cd /backend

# Create client_database.db if it doesn't exist
if [ ! -f client_database.db ]; then
  touch client_database.db
  echo "Created client_database.db"
fi

# Create app_database.db if it doesn't exist
if [ ! -f app_database.db ]; then
  touch app_database.db
  echo "Created app_database.db"
fi
