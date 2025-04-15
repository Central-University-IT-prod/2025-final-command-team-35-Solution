import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "haraka"
port = 25

def send_email(target, subject, content):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = "noreply@prod-team-35-lg7sic6v.REDACTED"
    message["To"] = target
    text = MIMEText(content)
    message.attach(text)

    with smtplib.SMTP(smtp_server, port) as server:
        server.login("MFS", os.getenv("SMTP_PASSWORD"))
        server.sendmail("noreply@prod-team-35-lg7sic6v.REDACTED", target, message.as_string())