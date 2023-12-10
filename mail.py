"""
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    """
    """
    senderEmail = 'support@orino.tech'

    def sendResetPass(self, receiverEmail, token):
        """
        """
        message = MIMEMultipart()
        message["From"] = EmailSender.senderEmail
        message["To"] = receiverEmail
        message["Subject"] = 'Reset Your Password'

        with open(f"email/resetpass.html", "r") as html_file:
            htmlContent = html_file.read()
            htmlContent = htmlContent.replace('{{ token }}', token)
            htmlPart = MIMEText(htmlContent, "html")
            message.attach(htmlPart)

        with smtplib.SMTP("localhost", 25) as server:
            server.sendmail(EmailSender.senderEmail, receiverEmail, message.as_string())

    def verifyEmail(self, receiverEmail, username, token):
        """
        """
        message = MIMEMultipart()
        message["From"] = EmailSender.senderEmail
        message["To"] = receiverEmail
        message["Subject"] = 'Verify Your Email'

        with open(f"email/confirmemail.html", "r") as html_file:
            htmlContent = html_file.read()
            htmlContent = htmlContent.replace('{{ username }}', username)
            htmlContent = htmlContent.replace('{{ token }}', token)
            htmlPart = MIMEText(htmlContent, "html")
            message.attach(htmlPart)

        with smtplib.SMTP("localhost", 25) as server:
            server.sendmail(EmailSender.senderEmail, receiverEmail, message.as_string())


# this awkward will be chnaged just to prevent any naming conflict in app.py
esmtp = EmailSender()
