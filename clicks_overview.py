import streamlit as st
import pandas as pd
import requests


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

analytics_display()
