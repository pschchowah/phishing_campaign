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

    st.subheader("Target Selection")

    # Add file uploader for the target list
    uploaded_file = st.file_uploader("Upload Target List (CSV)", type="csv")

    if uploaded_file:

        try:
            df = pd.read_csv(uploaded_file)
            if 'df' not in st.session_state:
                st.session_state['df'] = df

            # Form to manually add new entries

            with st.form(key="add_new_entry"):
            
                st.subheader("Add New Target Manually")
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    email = st.text_input("Email")
                
                with col2:
                    business_unit = st.text_input("Proximus Business Unit")
                    team_name = st.text_input("Proximus Team")
                    language = st.text_input("Language")
                
                submit_button = st.form_submit_button(label='Add Entry')

                if submit_button:
                    new_entry = {
                        "Email": email,
                        "First Name": first_name,
                        "Last Name": last_name,
                        "Proximus Business Unit": business_unit,
                        "Proximus Team": team_name,
                        "Language": language
                    }

                    df_new = pd.DataFrame(new_entry, index=[0])
                    st.session_state['df'] = pd.concat([st.session_state['df'], df_new], ignore_index=True)

                    st.success("New entry added successfully!")

            # Filter Selection

            with st.form(key="filter_selection"):
    
                st.subheader("Filter Selection")
                
                filter_columns = [
                    col for col in st.session_state['df'].columns if col != "First Name" and col != "Last Name"
                ]

                if "filters" not in st.session_state:
                    st.session_state["filters"] = {}

                for column in filter_columns:
                    unique_values = st.session_state['df'][column].dropna().unique()
                    selected_values = st.multiselect(
                        f"Filter by {column}",
                        unique_values,
                        default=st.session_state["filters"].get(column, [])
                    )

                    if selected_values:
                        st.session_state["filters"][column] = selected_values
                    elif column in st.session_state["filters"]:
                        del st.session_state["filters"][column]

                # Apply filters to the dataframe
                filtered_df = st.session_state['df']
                if "filters" in st.session_state:
                    for column, values in st.session_state["filters"].items():
                        filtered_df = filtered_df[filtered_df[column].isin(values)]
                
                submit_button = st.form_submit_button(label='Apply Filters')

                if submit_button:

                    st.session_state['df'] = filtered_df
                    st.success("Filters applied successfully!")

            # Launch button

            if st.button("Launch Campaign"):
                if not campaign_name:
                    st.error("Please provide a campaign name")
                elif st.session_state['filters'] == {}:
                    st.error("Please apply filters to select targets")
                else:
                    try:
                        with st.spinner("Creating campaign..."):
                            # First create the campaign in the database
                            
                            for column, values in st.session_state["filters"].items():
                                st.session_state['df'] = st.session_state['df'][st.session_state['df'][column].isin(values)]

                            # Get target count
                            target_count = len(st.session_state['df'])
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

                            for _, row in st.session_state['df'].iterrows():
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
                                    st.session_state['df'],
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
