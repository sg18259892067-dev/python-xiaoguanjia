import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from email_config import EMAIL_ADDRESS, EMAIL_PASSWORD


def send_email(subject, content, to_email):
    # 读取邮件模板
    with open("templates/daily.txt", "r", encoding="utf-8") as f:
        template = f.read()

    body = template.replace(
        "{{ date }}", datetime.now().strftime("%Y-%m-%d")
    ).replace(
        "{{ content }}", content
    )

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

