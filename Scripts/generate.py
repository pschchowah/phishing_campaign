import random
from datetime import datetime, timedelta
import pandas as pd

class Generator:
    def __init__(self, model=None, base_url="https://email-tracker-webservice.onrender.com"):
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
            {"Reason": "Unusual Login Activity Detected"},
            {"Reason": "Service Upgrade Notification"},
            {"Reason": "Salary Adjustment Notice"},
            {"Reason": "New Security Features Available"},
            {"Reason": "Mandatory Account Verification"},
            {"Reason": "Upcoming Maintenance Notice"},
            {"Reason": "Your Account Storage Limit Reached"},
            {"Reason": "Exclusive Webinar on Proximus AI Solutions"}
        ]

        # Load the CSV data for sender names

        self.model = model
        self.base_url = base_url

    def random_sender(self):
        """Selects a random sender's first and last name from the CSV dataset."""
        while True:
            sender_row = self.csv_data.sample(1).iloc[0]
            sender_first_name = sender_row["First Name"]
            sender_last_name = sender_row["Last Name"]
            # Ensure the sender is not the same as the receiver
            if sender_first_name != self.parameters["name"] and sender_last_name != self.parameters["surname"]:
                return sender_first_name, sender_last_name

    def define_body_prompt(self):
        """Generates the email body prompt, including dynamic content."""
        random_pick = random.choice(self.patterns)
        random_topic = self.random_topic()
        sender_first_name, sender_last_name = self.random_sender()
        click_tracking_url = f"{self.base_url}/track_click?email={self.parameters['email']}"

        # Define the email content with placeholders replaced
        self.prompt = (      
            f"Compose a professional email from {sender_first_name} {sender_last_name} to {self.parameters['name']} {self.parameters['surname']} "
            f"from the {self.parameters['team_name']} team. The email should address the following topic: {random_pick['Reason']}."
            f"The email should include the following elements:"
            f"1. A clear explanation of why {random_pick['Reason']} is critical, with specific consequences if no action is taken."
            f"2. A specific call to action requiring the recipient to click this link: <a href=\"{click_tracking_url}\">{random_pick['Fake Link']}</a>"
            f"3. Include a deadline with a random date and time in the near-future, excluding weekends."
            f"4. Ensure the tone is professional, urgent if necessary, but not overly alarming to avoid suspicion."
            
            f"Remember to:"
            f"- Use realistic and natural-sounding language throughout, avoiding repetitive or template-like phrases."
            f"- Keep the tone professional and approachable, like a helpful colleague."
            f"- Make the email appear tailored specifically for the recipient ({self.parameters['name']} {self.parameters['surname']})."
            f"- Format the result as an HTML body text with only <p> tags to subdivise in paragraphs." 
            f"- Format the date and time between <strong> tags to highlight it."

            f"Only write the body of the email. Do not include headers or signatures."
        )
        
        return self.prompt

    def generate_body_with_tracking(self):
        """Generates the body of the phishing email with tracking links and pixel."""
        body_prompt = self.define_body_prompt()
        body = self.generate_text(body_prompt)
        print(body)

        # Add tracking pixel and clickable link URLs
        tracking_pixel_url = f"{self.base_url}/track_open?email={self.parameters['email']}"

        # HTML version with tracking links and pixel, ensure proper line breaks and clickable links
        body_html = f"""
        <html>
            <body>
                <p>{body}</p>
                <br>
                <p><img src="{tracking_pixel_url}" width="1" height="1" style="display:none;" /></p>
            </body>
        </html>
        """

        return body_html, body

    def generate_text(self, prompt):
        """Generates content based on the provided prompt using the model."""
        if not self.model:
            raise ValueError("Model is not initialized. Please initialize the model first.")
        # Assuming the model has a method generate_content that returns the text response
        response = self.model.generate_content(prompt)
        return response.text