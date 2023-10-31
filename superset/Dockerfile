# Define base image
FROM apache/superset:3.0.1

# Switching to root to install the required packages
USER root

# Define additional environment variables to be used 
ENV ADMIN_EMAIL admin@example.com
ENV ADMIN_USERNAME admin
ENV ADMIN_PASSWORD adminpassword

# Add custom superset_config.py file and shell files
COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

COPY superset_custom.sh /app/superset_custom.sh
RUN chmod +x /app/superset_custom.sh

# Switching back to using the `superset` user
USER superset
ENTRYPOINT [ "/app/superset_custom.sh" ]
