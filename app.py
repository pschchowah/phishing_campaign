import streamlit as st
import pandas as pd
from Scripts.config import Configurator
from Scripts.generate import Generator
from Scripts.email import Emailer
import requests

# Streamlit App
st.set_page_config(page_title="Phishing Campaign Manager")

def login_page():
    st.title("Phishing Campaign Manager")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    # Fetch credentials from Streamlit secrets
    stored_username = st.secrets["authentication"]["username"]
    stored_password = st.secrets["authentication"]["password"]

    if login_button:
        if username == stored_username and password == stored_password:
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password")

# Sidebar Inputs
def sidebar_inputs():
    st.sidebar.title("Campaign Controls")

    # File Upload
    uploaded_file = st.sidebar.file_uploader("Upload Dataset (CSV)", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state["uploaded_data"] = df
        st.sidebar.success("Dataset uploaded successfully!")

    # Filter Selection
    if "uploaded_data" in st.session_state:
        df = st.session_state["uploaded_data"]
        filter_columns = df.columns

        for column in filter_columns:
            unique_values = df[column].dropna().unique()
            selected_values = st.sidebar.multiselect(f"Filter by {column}", unique_values)

            if selected_values:
                if "filters" not in st.session_state:
                    st.session_state["filters"] = {}
                st.session_state["filters"][column] = selected_values

    # Launch Button
    if st.sidebar.button("Launch Campaign"):
        if "uploaded_data" in st.session_state:
            launch_campaign()
        else:
            st.sidebar.error("Please upload a dataset before launching.")

# Campaign Launch Logic
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

    st.sidebar.success("Authentication successful. Campaign launched.")

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

    st.sidebar.success("Emails sent successfully!")

# Analytics Display
def analytics_display():
    st.title("Campaign Analytics")

    # Fetch data from external endpoint
    endpoint_url = "https://email-tracker-webservice.onrender.com/clicks"
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        tracking_data = pd.DataFrame(response.json())
        st.dataframe(tracking_data)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch analytics data: {e}")

# Main Application Logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    # Add Logout Button
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.sidebar.info("You have been logged out.")

    sidebar_inputs()
    analytics_display()