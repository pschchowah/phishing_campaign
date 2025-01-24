import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from io import StringIO


# Add project root to Python path
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))
from services.launch import launch_campaign
from api_client import APIClient
from services.generate import Generator

gen = Generator()


def campaign_launch_form():

    # Extract reasons and links from patterns
    reasons = [pattern["Reason"] for pattern in gen.patterns]
    links = [pattern["Fake Link"] for pattern in gen.patterns]
    
    # Campaign details section
    st.subheader("Campaign Details")
    with st.form(key="campaign_form"):
        
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
        col1, col2 = st.columns(2)
        
        with col1:
            # Fake Reason selection or input
            reason_selection_mode = st.radio(
                "How would you like to provide the Fake Reason?",
                options=["Choose from list", "Input manually"],
                index=0,
                help="Select whether to choose a reason from the list or input your own.",
            )

            if reason_selection_mode == "Choose from list":
                fake_reason = st.multiselect(
                    "Fake Reason",
                    reasons,
                    default=[reasons[0]],
                    help="Required - A unique fake reason for your campaign.",
                )
            else:
                fake_reason_input = st.text_input(
                    "Enter Fake Reason", help="Required - PRESS ENTER FOR VALIDATION."
                )
                fake_reason = [fake_reason_input] if fake_reason_input.strip() else []
        
        with col2:
            # Fake Link selection or input
            link_selection_mode = st.radio(
                "How would you like to provide the Fake Link?",
                options=["Choose from list", "Input manually"],
                index=0,
                help="Select whether to choose a link from the list or input your own.",
            )

            if link_selection_mode == "Choose from list":
                fake_link = st.multiselect(
                    "Fake Link",
                    links,
                    default=[links[0]],
                    help="Required - A unique fake link for your campaign.",
                )
            else:
                fake_link_input = st.text_input(
                    "Enter Fake Link", help="Required - PRESS ENTER FOR VALIDATION."
                )
                fake_link = [fake_link_input] if fake_link_input.strip() else []
        
        submit_button = st.form_submit_button(label="Submit Campaign Details")

        if submit_button:
            # Validation for fake reason and fake link
            if fake_reason and fake_link:
                st.success("Campaign details submitted successfully!")
                # Further processing of the form data can be added here
            else:
                st.error(
                    "Please provide valid inputs for both Fake Reason and Fake Link."
                )

    
    st.subheader("Target Selection")
    with st.form(key="target_selection_form"):

        # Add file uploader for the target list
        uploaded_file = st.file_uploader("Upload Target List (CSV)", type="csv")

        # Submit button for the form
        submit_button = st.form_submit_button(label="Submit Target List")

    if submit_button and uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            # Filter Selection
            st.subheader("Filter Selection")
            with st.form(key="filter_selection_form"):
                filter_columns = [
                    col for col in df.columns if col != "First Name" and col != "Last Name"
                ]
                for column in filter_columns:
                    unique_values = df[column].dropna().unique()
                    selected_values = st.multiselect(f"Filter by {column}", unique_values)

                    if selected_values:
                        if "filters" not in st.session_state:
                            st.session_state["filters"] = {}
                        st.session_state["filters"][column] = selected_values

                # Submit button for the form
                submit_button = st.form_submit_button(label="Apply Filters")

            if submit_button:
                # Apply filters to the dataframe
                if "filters" in st.session_state:
                    for column, values in st.session_state["filters"].items():
                        df = df[df[column].isin(values)]

                # Display the filtered dataframe
                st.dataframe(df)

            # Manual input for new employee
            st.subheader("Add New Employee Manually")
            with st.form(key="manual_employee_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    email = st.text_input("Email")
                
                with col2:
                    business_unit = st.text_input("Proximus Business Unit")
                    team_name = st.text_input("Proximus Team")
                    language = st.text_input("Language")
                
                submit_button = st.form_submit_button(label="Add Employee")

                if submit_button:
                    if not first_name or not last_name or not email:
                        st.error("Please provide all required fields (First Name, Last Name, Email)")
                    else:
                        employee_data = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "business_unit": business_unit,
                            "team_name": team_name,
                            "language": language,
                            "score": 0,
                        }
                        api_client.add_employee(employee_data)
                        st.success(f"Employee {first_name} {last_name} added successfully")

            # Launch button
            if st.button("Launch Campaign"):
                if not campaign_name:
                    st.error("Please provide a campaign name")
                else:
                    try:
                        with st.spinner("Creating campaign..."):
                            # First create the campaign in the database
                            if "filters" in st.session_state:
                                for column, values in st.session_state[
                                    "filters"
                                ].items():
                                    df = df[df[column].isin(values)]

                                # Get target count
                            target_count = len(df)
                            api_client = APIClient()
                            campaign = api_client.create_campaign(
                                name=campaign_name,
                                description=campaign_description or "",
                                target_count=target_count,
                            )

                            # Fetch the list of employees from the API
                            employees = api_client.get_employees()

                            # Extract email addresses from the JSON response
                            employee_emails = {
                                employee["email"] for employee in employees
                            }

                            # Initialize a counter for the number of employees added
                            employees_added_count = 0

                            for _, row in df.iterrows():
                                if row["Email"] in employee_emails:
                                    continue
                                else:
                                    employee_data = {
                                        "first_name": row["First Name"],
                                        "last_name": row["Last Name"],
                                        "email": row["Email"],
                                        "business_unit": row.get(
                                            "Proximus Business Unit", ""
                                        ),
                                        "team_name": row.get("Proximus Team", ""),
                                        "score": 0,
                                    }
                                    # Add new employee via API
                                    api_client.add_employee(employee_data)
                                    employees_added_count += 1

                            # Display the number of employees added
                            st.success(
                                f"Count of new employees: {employees_added_count}"
                            )

                            # Then launch the emails using the service
                            with st.spinner("Sending emails..."):
                                # Apply Filters
                                # Apply the filter on the DataFrame
                                launch_campaign(
                                    campaign_name,
                                    campaign_description or "",
                                    df,
                                    campaign["id"],
                                    fake_reason,
                                    fake_link,
                                )

                        st.success(f"Campaign '{campaign_name}' launched successfully!")
                        st.info(f"Campaign targets: {target_count}")
                    except Exception as e:
                        st.error(f"Error launching campaign: {str(e)}")

        except Exception as e:
            st.error(f"Error processing CSV file: {str(e)}")
    else:
        st.info("Please upload a CSV file containing the target list")


campaign_launch_form()
