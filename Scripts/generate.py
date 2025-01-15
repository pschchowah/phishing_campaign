import random
from datetime import datetime, timedelta
import pandas as pd

class Generator:

    def __init__(self, parameters=None, patterns=None, model=None, csv_file="data/dummy-emails - Sheet1.csv"):
        # Default parameters for the receiver
        self.parameters = parameters or {
            "name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "business_unit": "Business Solutions",
            "team_name": "Operations Team"
        }

        # Default phishing patterns
        self.patterns = patterns or [
            {"Reason": "Account Suspicious Activity", "Fake Link": "https://datalog.com/secure-login"},
            {"Reason": "Password Expiry Notification", "Fake Link": "https://thevault.com/reset-password"},
            {"Reason": "Exclusive Training Webinar", "Fake Link": "https://webinary.com/join-webinar"},
            {"Reason": "Email Storage Full", "Fake Link": "https://storee.com/manage-storage"}
        ]

        # Load the CSV data for sender names
        self.csv_data = pd.read_csv(csv_file)
        self.prompt = None
        self.model = model

    def random_date_and_time(self):

        """Generates a random future date and time."""
        future_date = datetime.now() + timedelta(days=random.randint(1, 30))
        random_time = f"{random.randint(8, 17)}:{random.choice(['00', '15', '30', '45'])} ET"
        return future_date.strftime("%A, %B %d, %Y"), random_time

    def random_topic(self):

        """Generates a random webinar topic."""
        topics = ["AI Trends in 2025", "Machine Learning Best Practices", "Optimizing Your AI Workflows"]
        return random.choice(topics)

    def random_sender(self):

        """Selects a random sender's first and last name from the CSV dataset, ensuring they are not the same as the receiver."""
        while True:
            sender_row = self.csv_data.sample(1).iloc[0]
            sender_first_name = sender_row["First Name"]
            sender_last_name = sender_row["Last Name"]
            
            # Check if the sender is the same as the receiver
            if sender_first_name != self.parameters["name"] and sender_last_name != self.parameters["surname"]:
                return sender_first_name, sender_last_name

    def define_body_prompt(self):

        # Randomly pick a pattern
        random_pick = random.choice(self.patterns)
        random_date, random_time = self.random_date_and_time()
        random_topic = self.random_topic()
        sender_first_name, sender_last_name = self.random_sender()

        # Replace placeholders with dynamic values
        self.prompt = (
            f"Write an email from {sender_first_name} {sender_last_name} to {self.parameters['name']} {self.parameters['surname']} "
            f"from the {self.parameters['team_name']} team on the following theme: {random_pick['Reason']}.\n\n"
            f"They should click on this link: {random_pick['Fake Link']}.\n\n"
            f"Include a recommendation of webinar about topic : {random_pick['Reason']} and schedule it for {random_date} at {random_time} and use this link : https://webinary.com/join-webinar and precise the webinar is additional for training."
            f"Only write the body of this email."
        )
        return self.prompt

    def generate_text(self, prompt):

        self.prompt = prompt
        if not self.model:
            raise ValueError("Model is not initialized. Call 'Configurator.initialize_model()' first.")

        if not self.prompt:
            raise ValueError("Prompt is not defined. Call 'define_prompt()' first.")

        response = self.model.generate_content(self.prompt)
        return response.text
