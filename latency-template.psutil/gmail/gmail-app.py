# Simple program that sends an email.

# Imported Classes
from email.message import EmailMessage
from smtplib import SMTP

# email.message documentation: https://docs.python.org/3/library/email.message.html
# smtplib documentation: https://docs.python.org/3/library/smtplib.html

class EmailNotification:
    def __init__(self, sender, password) -> None:
        self.sender = sender
        self.password = password

    def send_email(self, to, subject, body):
        # Create instances.
        msg = EmailMessage()
        server = SMTP(host="smtp.gmail.com", port=587)

        # Message details.
        msg["to"] = to
        msg["subject"] = subject
        msg["from"] = self.sender
        msg.set_content(body)

        # Sending message.
        server.starttls()
        server.login(self.sender, self.password)
        server.send_message(msg)
        print("Email sent.")
        server.quit()

# notifier = EmailNotification("kaffe.alert@gmail.com", "drpbnzkgiudlgngv")
# notifier.send_email(to="tomtelav@gmail.com", subject="Varning!", body="Ditt kaffe börjar bli kallt!")
# david.sl@hotmail.se
# A1$WVq20oZIpD6M8<*n/
