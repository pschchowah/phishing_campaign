from services.config import Configurator
from services.generate import Generator
from services.email import Emailer
import pandas as pd
import time


class Training:
    def __init__(self):
        """
        Initialize the Training class and its dependent services.
        """
        self.config = Configurator()
        self.generator = None
        self.email = None

    def initialize_services(self):
        """
        Initialize the required services: Configurator, Generator, and Emailer.
        """
        self.config.connect()
        self.config.initialize_model()
        self.generator = Generator(model=self.config.model)
        self.email = Emailer()
        self.email.authenticate()

    @staticmethod
    def filter_recipients(df: pd.DataFrame,
                          actions: list) -> pd.DataFrame:
        """
        Filters the DataFrame to include only recipients who match the specified actions.

        :param df: The DataFrame containing event data with an 'event' column.
        :param actions: A list of actions to filter (e.g., ['opened', 'clicked']).
        :return: A filtered DataFrame.
        """
        if "event" not in df.columns:
            raise ValueError(
                "The provided DataFrame must have an 'event' column for filtering.")

        filtered_df = df[df["event"].isin(actions)]
        return filtered_df

    def launch_training(
            self,
            training_name: str,
            description: str,
            df: pd.DataFrame,
            training_id: int,
            reason: str,
            link: str,
            actions_to_filter: list = None,
    ) -> dict:
        """
        Launches a training email campaign targeting users based on specific actions.

        :param training_name: Name of the training program.
        :param description: Description of the training campaign.
        :param df: The DataFrame containing recipient details and events.
        :param training_id: The unique ID of the training.
        :param reason: Reason or message content for the training email.
        :param link: Tracking link for the training program.
        :param actions_to_filter: List of actions to filter recipients (e.g., ['opened', 'clicked']).
        :return: A dictionary indicating the success status and training ID.
        """

        # Filter recipients if actions are provided
        if actions_to_filter:
            try:
                df = self.filter_recipients(df,
                                            actions_to_filter)
                if df.empty:
                    return {"status": "failure",
                            "message": "No recipients match the specified actions.",
                            "training_id": training_id}
            except ValueError as e:
                return {"status": "failure",
                        "message": str(e),
                        "training_id": training_id}

        # Initialize services
        self.initialize_services()

        # Send training emails
        for _, row in df.iterrows():
            time.sleep(
                1)  # Avoid overwhelming the email service

            receiver_name = row["First Name"]
            receiver_surname = row["Last Name"]

            self.generator.parameters = {
                "name": receiver_name,
                "surname": receiver_surname,
                "email": row["Email"],
                "business_unit": row.get(
                    "Proximus Business Unit", ""),
                "team_name": row.get("Proximus Team", ""),
            }

            # Generate email content with training tracking
            body_html, body = self.generator.generate_body_with_tracking(
                training_id, reason, link)

            subject = self.generator.generate_text(
                f"Write the subject for this email in 5 words with 'Training -' at the beginning : {body}"
            )

            sender = "me"
            recipient = row["Email"]
            message = self.email.create_message(sender,
                                                recipient,
                                                subject,
                                                body,
                                                body_html)
            self.email.send_message(message)

        return {"status": "success",
                "training_id": training_id}

if __name__ == "__main__":
    # Sample recipient data
    recipient_data = pd.DataFrame({
        "First Name": ["Alice", "Bob", "Charlie"],
        "Last Name": ["Smith", "Brown", "Davis"],
        "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
        "event": ["opened", "clicked", "attachment_opened"],
        "Proximus Business Unit": ["IT", "Sales", "Marketing"],
        "Proximus Team": ["Team A", "Team B", "Team C"]
    })

    # Define actions to filter
    actions = ["opened", "clicked", "attachment_opened"]

    # Launch training campaign
    campaign = Training()
    result = campaign.launch_training(
        training_name="Proximus Security Training",
        description="Email campaign for security training",
        df=recipient_data,
        training_id=456,
        reason="Complete your mandatory security training",
        link="https://training.proximus.com",
        actions_to_filter=actions
    )

    print(result)