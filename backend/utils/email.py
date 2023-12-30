from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, TrackingSettings, ClickTracking
from typing import List

from settings import APP_ENV, APP_HOST, SENDGRID_API_KEY


async def send_password_reset_email_with_sendgrid(email: List[str], token: str):
    message = Mail(
        from_email="no-reply@docshow.ai",
        to_emails=email,
        subject="DocShow AI - Password Reset Request",
        html_content=f'Click on the link to reset your password: <a href="https://{APP_HOST}/reset-password?token={token}">https://{APP_HOST}/reset-password</a>',
    )
    # Disable click tracking in development
    if APP_ENV == "development":
        message.tracking_settings = TrackingSettings()
        message.tracking_settings.click_tracking = ClickTracking(False, False)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = await sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))


async def send_verification_email_with_sendgrid(email: List[str], token: str):
    message = Mail(
        from_email="no-reply@docshow.ai",
        to_emails=email,
        subject="DocShow AI - Email Verification",
        html_content=f'Click on the link to verify your email: <a href="https://{APP_HOST}/verify-email?token={token}">https://{APP_HOST}/verify-email</a>',
    )
    # Disable click tracking in development
    if APP_ENV == "development":
        message.tracking_settings = TrackingSettings()
        message.tracking_settings.click_tracking = ClickTracking(False, False)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = await sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
