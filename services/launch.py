from services.config import Configurator
from services.generate import Generator
from services.email import Emailer
import pandas as pd
import time


def launch_campaign(
    campaign_name: str, description: str, df: pd.DataFrame, campaign_id: int, reason, link
):
    """
    Launches a phishing campaign with the given parameters and target list.
    Campaign must already exist in the database.
    """

    # Initialize services
    config = Configurator()
    config.connect()
    config.initialize_model()

    generator = Generator(model=config.model)
    email = Emailer()
    email.authenticate()

    # Send emails
    for _, row in df.iterrows():
        time.sleep(5)

        receiver_name = row["First Name"]
        receiver_surname = row["Last Name"]

        generator.parameters = {
            "name": receiver_name,
            "surname": receiver_surname,
            "email": row["Email"],
            "business_unit": row.get("Proximus Business Unit", ""),
            "team_name": row.get("Proximus Team", ""),
            "language": row["Language"]
        }

        # Generate email with campaign tracking
        body_html, body = generator.generate_body_with_tracking(campaign_id, reason, link)

        subject = generator.generate_text(
            f"Write the subject for this email in 5 words with 'Proximus -' at the beginning : {body}"
        )

        sender = "me"
        recipient = row["Email"]
        message = email.create_message(sender, recipient, subject, body, body_html)
        email.send_message(message)

    return {"status": "success", "campaign_id": campaign_id}
