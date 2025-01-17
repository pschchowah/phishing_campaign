import streamlit as st
import pandas as pd
from Scripts.config import Configurator
from Scripts.generate import Generator
from Scripts.email import Emailer

# Streamlit App
st.set_page_config(page_title="Phishing Campaign Manager", layout="wide")

def login_page():
    col1, col2, col3 = st.columns(3)

    with col2:
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


# Main Application Logic
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.sidebar.info("You have been logged out.")
    pg = st.navigation([st.Page("homepage.py"),st.Page("email_dashboard.py"), st.Page("clicks_overview.py")])
    pg.run()
    