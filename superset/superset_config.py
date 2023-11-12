from flask_appbuilder.security.views import expose
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.manager import BaseSecurityManager
from flask_appbuilder.security.manager import AUTH_REMOTE_USER
from flask import  redirect, request, flash
from flask_login import login_user

import os

SECRET_KEY = os.environ.get("SECRET_KEY")
SECURE_TOKEN = os.environ.get("SECURE_TOKEN")

# Turned off for superset dev, insecure
# Without these settings, we receive the following issue: flask_wtf.csrf.CSRFError: 400 Bad Request: The CSRF session token is missing.
# TODO: Configure csrf to work in PROD
WTF_CSRF_ENABLED = False
TALISMAN_ENABLED = False

ENABLE_JAVASCRIPT_CONTROLS = True

# Create a custom view to authenticate the user
AuthRemoteUserView=BaseSecurityManager.authremoteuserview
class CustomAuthUserView(AuthRemoteUserView):
    @expose('/login/')
    def login(self):
        print(f"Request url: {request.url}")
        token = request.args.get('token')
        next = request.args.get('next')
        sm = self.appbuilder.sm
        session = sm.get_session
        user = session.query(sm.user_model).filter_by(username='admin').first()
        print(f"Token: {token}\nSToken: {SECURE_TOKEN}\nNext: {next}\nUser: {user}")
        if token == SECURE_TOKEN:
            login_user(user, remember=False, force=True)
            if (next is not None):
                print(f"Next is not null, redirecting...")
                return redirect(next)
            else:
                print(f"Next is null, redirecting...\nRedirect url: {self.appbuilder.get_url_for_index}")
                return redirect(self.appbuilder.get_url_for_index)
        else:
            flash('Unable to auto login', 'warning')
            return super(CustomAuthUserView,self).login()

# Create a custom Security manager that overrides the CustomAuthUserView
class CustomSecurityManager(SupersetSecurityManager):
    authremoteuserview = CustomAuthUserView

# Use our custom authenticator
CUSTOM_SECURITY_MANAGER = CustomSecurityManager

# User remote authentication
AUTH_TYPE = AUTH_REMOTE_USER