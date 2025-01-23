import sys
from pathlib import Path
import streamlit as st
from api_client import APIClient

root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

# Fetch data from external endpoint

def fetch_data():
    api_client = APIClient()
    tracking_data = api_client.get_events()
    campaigns_data = api_client.get_campaigns()
    employees_data = api_client.get_employees()
    return tracking_data, campaigns_data, employees_data

# Analytics Display
def analytics_display():
    st.title("Data Overview")

    # Fetch data
    tracking_data, campaigns_data, employees_data = fetch_data()

    # Create a selectbox for the user to choose which dataframe to display
    option = st.selectbox(
        'Select data to display',
        ('Tracking Data', 'Campaigns Data', 'Employees Data')
    )

    # Display the selected dataframe
    if option == 'Tracking Data':
        st.dataframe(tracking_data, use_container_width=True)
    elif option == 'Campaigns Data':
        st.dataframe(campaigns_data, use_container_width=True)
    elif option == 'Employees Data':
        st.dataframe(employees_data, use_container_width=True)

# Call the function to display analytics
analytics_display()