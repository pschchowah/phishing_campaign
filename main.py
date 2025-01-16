from Scripts.config import Configurator
from Scripts.generate import Generator
from Scripts.email import Emailer
import pandas as pd

def main():
    # Initialize the Configurator
    config = Configurator()
    config.connect()
    config.initialize_model()

    # Load the dataset
    df = pd.read_csv("data/dummy-emails - Sheet1.csv")

    # Initialize the Generator
    generator = Generator(model=config.model)

    # Initialize the Email
    email = Emailer()

    # Authenticate the email
    email.authenticate()
    print("Authentication successful.")

    # Loop through each row in the dataset and generate/send emails
    for _, row in df.iterrows():
        # Set parameters for the receiver's details
        receiver_name = row["First Name"]
        receiver_surname = row["Last Name"]

        generator.parameters = {
            "name": receiver_name,
            "surname": receiver_surname,
            "email": row["Email"],
            "business_unit": row["Proximus Business Unit"],
            "team_name": row["Proximus Team"]
        }

        # Generate body with tracking links
        body_html, body = generator.generate_body_with_tracking()
        
        # Generate email subject (you can customize this logic)
        subject = generator.generate_text(f"Write the subject for this email in 5 words with 'Proximus Training -' at the beginning : {body}")

        sender = "me"
        recipient = row["Email"]
        
        # Create the email message
        
        message = email.create_message(sender, recipient, subject, body, body_html)
        
        # Send the email
        email.send_message(message)

if __name__ == "__main__":
    main()