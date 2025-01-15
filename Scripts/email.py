import base64
import os.path
from email.mime.text import MIMEText

def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message):
    """Send an email message."""
    try:
        sent_message = (
            service.users()
            .messages()
            .send(userId=user_id, body=message)
            .execute()
        )
        print(f"Message sent! Message ID: {sent_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")