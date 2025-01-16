import random
from datetime import datetime, timedelta
import pandas as pd


class Generator:
    def __init__(self, model=None,
                 csv_file="data/dummy-emails - Sheet1.csv",
                 base_url="https://email-tracker-webservice.onrender.com"):
        # Default parameters for the receiver
        self.parameters = {
            "name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "business_unit": "Business Solutions",
            "team_name": "Operations Team"
        }

        # Default phishing patterns
        self.patterns = [
            {"Reason": "Unusual Login Activity Detected",
             "Fake Link": "https://login.proximus-secure.com"},
            {"Reason": "Service Upgrade Notification",
             "Fake Link": "https://update.proximus.com/upgrade"},
            {"Reason": "Salary Adjustment Notice",
             "Fake Link": "https://salary.proximus.com"},
            {"Reason": "New Security Features Available",
             "Fake Link": "https://security.proximus.com"},
            {"Reason": "Mandatory Account Verification",
             "Fake Link": "https://verify.proximus-account.com"},
            {"Reason": "Upcoming Maintenance Notice",
             "Fake Link": "https://maintenance.proximus.com"},
            {"Reason": "Your Account Storage Limit Reached",
             "Fake Link": "https://storage.proximus.com/manage"},
            {
                "Reason": "Exclusive Webinar on Proximus AI Solutions",
                "Fake Link": "https://webinars.proximus.com/join"}
        ]

        # Load the CSV data for sender names
        self.csv_data = pd.read_csv(csv_file)
        self.model = model
        self.base_url = base_url

    def random_date_and_time(self):
        """Generates a random future date and time."""
        future_date = datetime.now() + timedelta(
            days=random.randint(1, 30))
        random_time = f"{random.randint(8, 17)}:{random.choice(['00', '15', '30', '45'])} ET"
        return future_date.strftime(
            "%A, %B %d, %Y"), random_time

    def random_topic(self):
        """Generates a random webinar topic."""
        topics = ["AI Trends in 2025",
                  "Machine Learning Best Practices",
                  "Optimizing Your AI Workflows"]
        return random.choice(topics)

    def random_sender(self):
        """Selects a random sender's first and last name from the CSV dataset."""
        while True:
            sender_row = self.csv_data.sample(1).iloc[0]
            sender_first_name = sender_row["First Name"]
            sender_last_name = sender_row["Last Name"]
            # Ensure the sender is not the same as the receiver
            if sender_first_name != self.parameters[
                "name"] and sender_last_name != \
                    self.parameters["surname"]:
                return sender_first_name, sender_last_name

    def define_body_prompt(self):
        """Generates the email body prompt, including dynamic content."""
        random_pick = random.choice(self.patterns)
        random_date, random_time = self.random_date_and_time()
        random_topic = self.random_topic()
        sender_first_name, sender_last_name = self.random_sender()

        # Define the email content with placeholders replaced
        self.prompt = (
            f"Compose a professional email from {sender_first_name} {sender_last_name} to {self.parameters['name']} {self.parameters['surname']}"
            f"from the {self.parameters['team_name']} team. The email should address the following topic: {random_pick['Reason']}. "
            f"The email should include the following elements:\n"
            f"1. A clear explanation of why {random_pick['Reason']} is important.\n"
            f"2. A recommendation for a related webinar scheduled for {random_date} at {random_time}, GMT+1.\n"
            f"3. Keep the tone professional and urgent but not alarming.\n"
            f"Ensure the language sounds natural and is tailored for the recipient."
            f"Format the result as an HTML body text with only <p> tags to subdivise in paragraphs."
            f"Never add links directly, it will be implemented with static html afterwards.\n"
            )

        return self.prompt

    def generate_body_with_tracking(self):
        """Generates the body of the phishing email with tracking links and pixel."""
        body_prompt = self.define_body_prompt()
        body = self.generate_text(body_prompt)
        print(body)

        # Add tracking pixel and clickable link URLs
        tracking_pixel_url = f"{self.base_url}/track_open?email={self.parameters['email']}"
        click_tracking_url = f"{self.base_url}/track_click?email={self.parameters['email']}"

        # HTML version with tracking links and pixel, ensure proper line breaks and clickable links
        body_html = f"""
        <html>
            <body>
                <p>{body}</p>
                <p>How to access the webinar:</p>
                <p><a href="{click_tracking_url}" target="_blank"> https://webinars.proximus.com/join </a></p>
                <br>
                <p><img src="{tracking_pixel_url}" width="1" height="1" style="display:none;" /></p>
            </body>
        </html>
        """

        return body_html, body

    def generate_text(self, prompt):
        """Generates content based on the provided prompt using the model."""
        if not self.model:
            raise ValueError(
                "Model is not initialized. Please initialize the model first.")
        # Assuming the model has a method generate_content that returns the text response
        response = self.model.generate_content(prompt)
        return response.text
