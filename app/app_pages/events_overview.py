import streamlit as st
import pandas as pd
import requests
import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))
from api_client import APIClient


# Analytics Display
def analytics_display():
    st.title("Campaign Analytics")

    # Fetch data from external endpoint
    api_client = APIClient()
    tracking_data = api_client.get_events()
    campaigns_data = api_client.get_campaigns()
    #employees_data = api_client.get_employees()

    # Create a selectbox for the user to choose which dataframe to display
    option = st.selectbox(
        'Select data to display',
        ('Tracking Data', 'Campaigns Data', 'Employees Data')
    )

    # Display the selected dataframe
    if option == 'Tracking Data':
        st.dataframe(pd.DataFrame(tracking_data))
    elif option == 'Campaigns Data':
        st.dataframe(pd.DataFrame(campaigns_data))
    # elif option == 'Employees Data':
    #     st.dataframe(pd.DataFrame(employees_data))

analytics_display()
