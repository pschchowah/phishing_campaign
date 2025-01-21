import random
from datetime import datetime, timedelta
import pandas as pd
import os


class Generator:
    def __init__(
        self,
        model=None,
        csv_file="data/dummy-emails - Sheet1.csv",
        base_url="http://localhost:8000",
    ):
        # Default parameters for the receiver
        self.parameters = {
            "name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "business_unit": "Business Solutions",
            "team_name": "Operations Team",
        }

        # Default phishing patterns
        self.patterns = [
            {
                "Reason": "Unusual Login Activity Detected",
                "Fake Link": "https://login.proximus-secure.com",
            },
            {
                "Reason": "Service Upgrade Notification",
                "Fake Link": "https://update.proximus.com/upgrade",
            },
            {
                "Reason": "Salary Adjustment Notice",
                "Fake Link": "https://salary.proximus.com",
            },
            {
                "Reason": "New Security Features Available",
                "Fake Link": "https://security.proximus.com",
            },
            {
                "Reason": "Mandatory Account Verification",
                "Fake Link": "https://verify.proximus-account.com",
            },
            {
                "Reason": "Upcoming Maintenance Notice",
                "Fake Link": "https://maintenance.proximus.com",
            },
            {
                "Reason": "Your Account Storage Limit Reached",
                "Fake Link": "https://storage.proximus.com/manage",
            },
            {
                "Reason": "Exclusive Webinar on Proximus AI Solutions",
                "Fake Link": "https://webinars.proximus.com/join",
            },
        ]

        # Load the CSV data for sender names
        self.csv_data = pd.read_csv(csv_file)
        self.model = model
        self.base_url = base_url

    def random_date_and_time(self):
        """Generates a random future date and time."""
        future_date = datetime.now() + timedelta(days=random.randint(1, 30))
        random_time = (
            f"{random.randint(8, 17)}:{random.choice(['00', '15', '30', '45'])} ET"
        )
        return future_date.strftime("%A, %B %d, %Y"), random_time

    def random_sender(self):
        """Selects a random sender's first and last name from the CSV dataset."""
        while True:
            sender_row = self.csv_data.sample(1).iloc[0]
            sender_first_name = sender_row["First Name"]
            sender_last_name = sender_row["Last Name"]
            # Ensure the sender is not the same as the receiver
            if (
                sender_first_name != self.parameters["name"]
                and sender_last_name != self.parameters["surname"]
            ):
                return sender_first_name, sender_last_name

    def define_body_prompt(self, campaign_id, reason, link):
        """Generates the email body prompt, including dynamic content."""
        future_date, random_time = self.random_date_and_time()
        sender_first_name, sender_last_name = self.random_sender()
        click_tracking_url = f"{self.base_url}/events/track_click?email={self.parameters['email']}&campaign_id={campaign_id}"

        # Define the email content with placeholders replaced
        self.prompt = (
            f"Compose a professional email from {sender_first_name} {sender_last_name} to {self.parameters['name']} {self.parameters['surname']} "
            f"from the {self.parameters['team_name']} team. The email should address the following topic: {reason}."
            f"The email should include the following elements:"
            f"1. A clear explanation of why {reason} is critical, with specific consequences if no action is taken."
            f"2. A specific call to action requiring the recipient to click this link: <a href=\"{click_tracking_url}\">{link}</a>"
            f"3. Include a deadline with a {future_date} and {random_time} in the near-future, excluding weekends."
            f"4. Ensure the tone is professional and not overly alarming to avoid suspicion."
            f"Remember to:"
            f"- Use realistic and natural-sounding language throughout, avoiding repetitive or template-like phrases."
            f"- Keep the tone professional and approachable, like a helpful colleague."
            f"- Make the email appear tailored specifically for the recipient ({self.parameters['name']} {self.parameters['surname']})."
            f"- Format the result as an HTML body text with only <p> tags to subdivise in paragraphs."
            f"- Format the date and time between <strong> tags to highlight it."
            f"Only write the body of the email. Do not include headers or signatures."
        )

        return self.prompt

    def generate_body_with_tracking(self, campaign_id, reason, link):
        """Generates the body of the phishing email with tracking links and pixel."""
        if not isinstance(campaign_id, int):
            raise ValueError("campaign_id must be an integer")

        body_prompt = self.define_body_prompt(campaign_id, reason, link)
        body = self.generate_text(body_prompt)

        # Create tracking pixel URL
        tracking_pixel_url = f"{self.base_url}/events/track_open?email={self.parameters['email']}&campaign_id={campaign_id}"

        # Create HTML body with a simple tracking pixel image
        body_html = f"""
            <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                </head>
                <body>
                    {body}
                    <img src="{tracking_pixel_url}" 
                        width="1" 
                        height="1" 
                        alt="" 
                        style="display:none">
                </body>
                <p> <a href="{self.base_url}/events/track_reported?email={self.parameters['email']}&campaign_id={campaign_id}"> Report phishing </a>  </p>
            </html>
        """

        return body_html, body
    
    def generate_fake_attachment(self, file_type="jpg", file_size_kb=100):
        """
        Generates a fake attachment file with random content.

        Args:
            file_type (str): The type of the file (e.g., 'pdf', 'docx', 'xlsx').
            file_size_kb (int): The size of the file in kilobytes.

        Returns:
            str: The file path of the generated fake attachment.
        """
        # Validate the file type
        valid_file_types = ["pdf", "docx", "xlsx", "txt", "jpg", "png"]
        if file_type not in valid_file_types:
            raise ValueError(f"Unsupported file type: {file_type}. Choose from {valid_file_types}.")

        # Generate a random file name
        file_name = f"attachment_{random.randint(1000, 9999)}.{file_type}"
        file_path = os.path.join("attachments", file_name)

        # Ensure the directory exists
        os.makedirs("attachments", exist_ok=True)

        # Generate random content to mimic a real file
        with open(file_path, "wb") as f:
            f.write(os.urandom(file_size_kb * 1024))  # Write random binary data

        return file_path

    def generate_text(self, prompt):
        """Generates content based on the provided prompt using the model."""
        if not self.model:
            raise ValueError(
                "Model is not initialized. Please initialize the model first."
            )
        # Assuming the model has a method generate_content that returns the text response
        response = self.model.generate_content(prompt)
        return response.text
