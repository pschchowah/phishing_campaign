from Scripts.config import Configurator
from Scripts.generate import Generator
import pandas as pd

def main():
    # Initialize the Configurator
    config = Configurator()
    config.connect()
    config.initialize_model()

    # Load the dataset (Optional: Replace with real data if needed)
    df = pd.read_csv("data/dummy-emails - Sheet1.csv")

    # Initialize the Generator
    generator = Generator(model=config.model)

    # Generate prompts and outputs for each user in the dataset
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
        
        # Define the prompt and generate email text
        prompt = generator.define_prompt()
        response = generator.generate_text()
        
        # Print the generated email
        print(f"\nEmail for {receiver_name} {receiver_surname}:\n{response}\n")

if __name__ == "__main__":
    main()