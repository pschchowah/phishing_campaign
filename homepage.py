import streamlit as st
import pandas as pd
from Scripts.config import Configurator
from Scripts.generate import Generator
from Scripts.email import Emailer

# Campaign Launch Logic
# Sidebar Inputs
def sidebar_inputs():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("Campaign Controls")

        # File Upload
        uploaded_file = st.file_uploader("Upload Dataset (CSV)", type="csv")

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.session_state["uploaded_data"] = df
            st.success("Dataset uploaded successfully!")

        # Filter Selection
        if "uploaded_data" in st.session_state:
            df = st.session_state["uploaded_data"]
            filter_columns = df.columns

            for column in filter_columns:
                unique_values = df[column].dropna().unique()
                selected_values = st.multiselect(f"Filter by {column}", unique_values)

                if selected_values:
                    if "filters" not in st.session_state:
                        st.session_state["filters"] = {}
                    st.session_state["filters"][column] = selected_values

        # Launch Button
        if st.button("Launch Campaign"):
            if "uploaded_data" in st.session_state:
                launch_campaign()
            else:
                st.error("Please upload a dataset before launching.")

def launch_campaign():
    df = st.session_state["uploaded_data"]

    # Apply Filters
    if "filters" in st.session_state:
        for column, values in st.session_state["filters"].items():
            df = df[df[column].isin(values)]

    # Initialize Configurator
    config = Configurator()
    config.connect()
    config.initialize_model()

    generator = Generator(model=config.model)
    email = Emailer()
    email.authenticate()

    st.success("Authentication successful. Campaign launched.")

    # Send Emails
    for _, row in df.iterrows():
        receiver_name = row["First Name"]
        receiver_surname = row["Last Name"]

        generator.parameters = {
            "name": receiver_name,
            "surname": receiver_surname,
            "email": row["Email"],
            "business_unit": row.get("Proximus Business Unit", ""),
            "team_name": row.get("Proximus Team", "")
        }

        body_html, body = generator.generate_body_with_tracking()
        subject = generator.generate_text(f"Write the subject for this email in 5 words with 'Proximus -' at the beginning : {body}")

        sender = "me"
        recipient = row["Email"]
        message = email.create_message(sender, recipient, subject, body, body_html)

        email.send_message(message)

    st.success("Emails sent successfully!")

sidebar_inputs()
