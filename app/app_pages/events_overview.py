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
    st.dataframe(pd.DataFrame(tracking_data))


analytics_display()
