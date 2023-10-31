# superset_config.py
SECRET_KEY = 'uwBS1V+RsmEiEdy7kkQ3Gcs4FnaaKhYOcqasXWd9uUjZ4ng1tn5XoBCw'  # Replace with your actual key

# Turned off for superset dev, insecure
# Without these settings, we receive the following issue: flask_wtf.csrf.CSRFError: 400 Bad Request: The CSRF session token is missing.
# TODO: Configure csrf to work in PROD
WTF_CSRF_ENABLED = False
TALISMAN_ENABLED = False