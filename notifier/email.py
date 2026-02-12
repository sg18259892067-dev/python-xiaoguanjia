import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path
from .base import Notifier

class EmailNotifier(Notifier):
    def send(self, title: str, content: str):
        smtp_server = os.getenv("SMTP_SERVER", "smtp.qq.com")
        smtp_port = int(os.getenv("SMTP_PORT", "465"))

        email_from = os.getenv("EMAIL_FROM")
        email_to = os.getenv("EMAIL_TO")
        auth_code = os.getenv("EMAIL_AUTH_CODE")

        if not all([email_from, email_to, auth_code]):
            raise RuntimeError("邮箱环境变量未配置完整")

        template_path = Path("templates/email.html")
        html = template_path.read_text(encoding="utf-8")

        html = html.replace("{{ title }}", title)
        html = html.replace("{{ content }}", content.replace("\n", "<br>"))

        msg = MIMEText(html, "html", "utf-8")
        msg["From"] = Header("小管家", "utf-8")
        msg["To"] = Header("你自己", "utf-8")
        msg["Subject"] = Header(title, "utf-8")

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_from, auth_code)
        server.sendmail(email_from, [email_to], msg.as_string())
        server.quit()
