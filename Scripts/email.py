import base64
import os.path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Emailer:
    def __init__(self, credentials_path="data/credentials.json", token_path="data/token.json"):
        """
        Initialize the Emailer class and authenticate with Gmail API.

        :param credentials_path: Path to the client secrets JSON file.
        :param token_path: Path to store or read the token file for user authentication.
        """
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = None

        self.authenticate()

    def authenticate(self):
        """Authenticate the user and initialize the Gmail API service."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(
                self.token_path, self.SCOPES
            )
        # If there are no valid credentials, prompt the user to log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, "w") as token_file:
                token_file.write(self.creds.to_json())

        # Build the Gmail API service
        self.service = build("gmail", "v1", credentials=self.creds)
        return self.service

    def create_message(self, sender, to, subject, message_text, message_html):
        """
        Create a MIME message for an email with both plain-text and HTML content.

        :param sender: The email address of the sender.
        :param to: The email address of the receiver.
        :param subject: The subject of the email.
        :param message_text: The plain-text body of the email.
        :param message_html: The HTML body of the email.
        :return: A dictionary containing the base64-encoded email message.
        """
        # Create a MIMEMultipart message
        message = MIMEMultipart("alternative")
        message["to"] = to
        message["from"] = sender
        message["subject"] = subject

        # Add plain-text and HTML versions of the email

        part_html = MIMEText(message_html, "html")
        part_plain = MIMEText(message_text, "plain")

        # Attach both parts to the message
        
        message.attach(part_plain)
        message.attach(part_html)

        # Return the raw base64-encoded message
        return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, message):
        """
        Send an email message.

        :param message: The message dictionary created by `create_message`.
        :return: The sent message response from the Gmail API.
        """
        try:
            sent_message = (
                self.service.users()
                .messages()
                .send(userId="me", body=message)
                .execute()
            )
            print(f"Message sent! Message ID: {sent_message['id']}")
            return sent_message
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None