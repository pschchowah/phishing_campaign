import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to Python path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))
from services.launch import launch_campaign
from api_client import APIClient


def campaign_launch_form():
    st.title("Campaign Launch")

    # Campaign details section
    st.subheader("Campaign Details")
    campaign_name = st.text_input(
        "Campaign Name",
        key="campaign_name",
        help="Required - A unique name for your campaign",
    )
    campaign_description = st.text_area(
        "Campaign Description",
        key="campaign_description",
        help="Optional - Add details about this campaign",
    )

    # Target selection section
    st.subheader("Target Selection")
    uploaded_file = st.file_uploader("Upload Target List (CSV)", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            # Display filters only if relevant columns exist
            filters_applied = False

            # Business Unit filter
            if "Proximus Business Unit" in df.columns:
                business_units = df["Proximus Business Unit"].dropna().unique()
                selected_units = st.multiselect(
                    "Filter by Business Unit", business_units
                )
                if selected_units:
                    df = df[df["Proximus Business Unit"].isin(selected_units)]
                    filters_applied = True

            # Team filter
            if "Proximus Team" in df.columns:
                teams = df["Proximus Team"].dropna().unique()
                selected_teams = st.multiselect("Filter by Team", teams)
                if selected_teams:
                    df = df[df["Proximus Team"].isin(selected_teams)]
                    filters_applied = True

            # Show filter summary
            if filters_applied:
                st.info(f"Number of targets after filtering: {len(df)}")
            else:
                st.info(f"Total number of targets: {len(df)}")

            # Launch button
            if st.button("Launch Campaign"):
                if not campaign_name:
                    st.error("Please provide a campaign name")
                else:
                    try:
                        with st.spinner("Creating campaign..."):
                            # First create the campaign in the database
                            api_client = APIClient()
                            campaign = api_client.create_campaign(
                                name=campaign_name,
                                description=campaign_description or "",
                            )

                            # Then launch the emails using the service
                            with st.spinner("Sending emails..."):
                                launch_campaign(
                                    campaign_name=campaign_name,
                                    description=campaign_description or "",
                                    df=df,
                                    campaign_id=campaign["id"],
                                )

                        st.success(f"Campaign '{campaign_name}' launched successfully!")
                    except Exception as e:
                        st.error(f"Error launching campaign: {str(e)}")

        except Exception as e:
            st.error(f"Error processing CSV file: {str(e)}")
    else:
        st.info("Please upload a CSV file containing the target list")


campaign_launch_form()
