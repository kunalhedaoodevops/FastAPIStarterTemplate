import smtplib
from email.message import EmailMessage
from app.core.config import settings


def send_reset_email(to_email: str, reset_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email

    msg.set_content(f"""
Hello,

Click the link below to reset your password:

{reset_link}

This link expires in 15 minutes.
""")

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
