import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from sqlalchemy.orm import Session



# Add project root to Python path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))
from services.launch import launch_campaign
from api_client import APIClient
from services.generate import Generator
from api.database import SessionLocal
from api import models, database

gen = Generator()


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

    # Extract reasons and links from patterns
    reasons = [pattern["Reason"] for pattern in gen.patterns]
    links = [pattern["Fake Link"] for pattern in gen.patterns]

    # Fake Reason selection or input
    reason_selection_mode = st.radio(
        "How would you like to provide the Fake Reason?",
        options=["Choose from list", "Input manually"],
        index=0,
        help="Select whether to choose a reason from the list or input your own."
    )

    if reason_selection_mode == "Choose from list":
        fake_reason = st.multiselect(
            "Fake Reason",
            reasons,
            default=[reasons[0]],
            help="Required - A unique fake reason for your campaign."
        )
    else:
        fake_reason = [st.text_input("Enter Fake Reason", help="Required - PRESS ENTER FOR VALIDATION.")]

    # Fake Link selection or input
    link_selection_mode = st.radio(
        "How would you like to provide the Fake Link?",
        options=["Choose from list", "Input manually"],
        index=0,
        help="Select whether to choose a link from the list or input your own."
    )

    if link_selection_mode == "Choose from list":
        fake_link = st.multiselect(
            "Fake Link",
            links,
            default=[links[0]],
            help="Required - A unique fake link for your campaign."
        )
    else:
        fake_link = [st.text_input("Enter Fake Link", help="Required - PRESS ENTER FOR VALIDATION.")]

    # Target selection section
    st.subheader("Target Selection")
    uploaded_file = st.file_uploader("Upload Target List (CSV)", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            # Filter Selection
            
            filter_columns = df.columns

            for column in filter_columns:
                unique_values = df[column].dropna().unique()
                selected_values = st.multiselect(f"Filter by {column}", unique_values)

                if selected_values:
                    if "filters" not in st.session_state:
                        st.session_state["filters"] = {}
                    st.session_state["filters"][column] = selected_values

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
                            # Process CSV and add employees to the database
                            db = SessionLocal()
                           # Initialize counter
                            added_count = 0

                            # Iterate through CSV
                            try:
                                for _, row in df.iterrows():
                                    email = row["Email"]
                                    # Check if the employee exists in the database
                                    existing_employee = db.query(models.Employee).filter(models.Employee.email == email).first()

                                    if not existing_employee:
                                        try:
                                            employee_data = {
                                            "first_name": row["First Name"],
                                            "last_name": row["Last Name"],
                                            "email": row["Email"],
                                            "business_unit": row.get("Proximus Business Unit", ""),
                                            "team_name": row.get("Proximus Team", ""),
                                            "score": 0,
                                        }                       
                                            # Add new employee via API
                                            api_client.add_employee(employee_data)
                                            added_count += 1
                                        except Exception as e:
                                            st.error(f"Failed to add employee {email}: {str(e)}")
                                    else:
                                        st.warning(f"Employee with email '{email}' already exists in the database")
                                
                                if added_count > 0:
                                    st.success(f"{added_count} new employees added successfully.")
                                else:
                                    st.info("No new employees were added.")
                            except Exception as e:
                                st.error(f"Error processing CSV: {str(e)}")
                                
                            # Then launch the emails using the service
                            with st.spinner("Sending emails..."):
                                # Apply Filters
                                if "filters" in st.session_state:
                                    for column, values in st.session_state["filters"].items():
                                        df = df[df[column].isin(values)]  # Apply the filter on the DataFrame
                                launch_campaign(
                                    campaign_name=campaign_name,
                                    description=campaign_description or "",
                                    df=df,
                                    campaign_id=campaign["id"],
                                    reason = fake_reason,
                                    link = fake_link
                                )

                        st.success(f"Campaign '{campaign_name}' launched successfully!")
                    except Exception as e:
                        st.error(f"Error launching campaign: {str(e)}")

        except Exception as e:
            st.error(f"Error processing CSV file: {str(e)}")
    else:
        st.info("Please upload a CSV file containing the target list")


campaign_launch_form()
