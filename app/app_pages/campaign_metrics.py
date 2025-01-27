import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import datetime
from pathlib import Path

# Add the parent directory to the python path to import custom modules
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))
from api_client import APIClient


def dataframe_creation() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetches events and campaigns data from an external API and creates corresponding DataFrames.
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Two DataFrames - events and campaigns data.
    """
    api_client = APIClient()
    tracking_data_events = api_client.get_events()
    tracking_data_campaigns = api_client.get_campaigns()
    return pd.DataFrame(tracking_data_events), pd.DataFrame(tracking_data_campaigns)


# Initialize dataFrames
events_df, campaigns_df = dataframe_creation()


def create_final_dataframe(
    events_df: pd.DataFrame, campaigns_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Combines events and campaigns data to create a final merged dataFrame with event counts.
    :params:
        events_df: dataFrame containing event data.
        campaigns_df: dataFrame containing campaign data.
    Returns:
        pd.DataFrame: merged dataFrame with event counts per campaign.
    """
    all_event_types = [
        "open",
        "click",
        "submitted",
        "downloaded_attachement",
        "reported",
    ]
    event_counts = (
        events_df.groupby(["campaign_id", "event_type"]).size().unstack(fill_value=0)
    )
    # Ensure all event types are represented
    for event in all_event_types:
        if event not in event_counts.columns:
            event_counts[event] = 0
    # Merge campaigns with event counts
    df = pd.merge(
        campaigns_df, event_counts, left_on="id", right_on="campaign_id", how="left"
    )
    df = df.fillna(0)  # Fill missing values with 0
    return df


# Create the merged DataFrame
merged_df = create_final_dataframe(events_df, campaigns_df)


# Pie charts
def pie_chart(data: float) -> None:
    """
    Displays a pie chart of a given percentage using Streamlit and Matplotlib.
    :params:
        data: percentage value to display in the pie chart.
    """
    st.markdown(f"### {data}%")
    percentage = [data, 100 - data]
    colors = ["#7d57a7", "#e6e6e7"]
    plt.pie(percentage, colors=colors, startangle=90)
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.axis("equal")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.clf()


def calculate_click_rate(
    campaign_clicks: int,
    campaign_opens: int,
    campaign_sent: int,
    campaign_submitted: int,
    campaign_reports: int,
    campaign_download: int,
) -> tuple[float, float, float, float, float]:
    """
    Calculates various campaign metrics as percentages.
    :params:
        campaign_clicks: Number of clicks.
        campaign_opens: Number of opens.
        campaign_sent: Total emails sent.
        campaign_submitted: Number of submissions.
        campaign_reports: Number of reports.
        campaign_download: Number of downloads.
    Returns:
        tuple[float, float, float, float, float]: Open rate, click rate, data submitted rate,
                                                  report rate, and download rate.
    """
    click_rate = round(campaign_clicks / campaign_sent * 100, 2)
    open_rate = round(campaign_opens / campaign_sent * 100, 2)
    data_submitted = round(campaign_submitted / campaign_sent * 100, 2)
    reports = round(campaign_reports / campaign_sent * 100, 2)
    downloads = round(campaign_download / campaign_sent * 100, 2)
    # Ensure rates do not exceed 100%
    if click_rate > 100:
        click_rate = 100
    if open_rate > 100:
        open_rate = 100
    if data_submitted > 100:
        data_submitted = 100
    if reports > 100:
        reports = 100
    if downloads > 100:
        downloads = 100
    return open_rate, click_rate, data_submitted, reports, downloads


def graphs(df: pd.DataFrame, events: pd.DataFrame) -> None:
    """
    Generates a Streamlit dashboard with graphs and metrics based on the campaign data.
    :params:
        df: Campaigns DataFrame with aggregated metrics.
        events: Events DataFrame for detailed event data.
    """
    # Process time data
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["month_word"] = df["created_at"].dt.strftime("%B")
    df["year"] = df["created_at"].dt.year
    df["day"] = df["created_at"].dt.day
    df["month"] = df["created_at"].dt.month
    df["date"] = pd.to_datetime(df[["day", "month", "year"]])

    # Sidebar for filters
    with st.sidebar:
        st.title("Phishing Email Dashboard")
        on = st.toggle("Per campaign", value=False)
        unique_years = df["year"].unique()
        years = st.segmented_control("Which year", options=unique_years)

        # Filter data based on year and month
        if years == None:
            df = df
        else:
            df = df[df["year"] == years]
            unique_months = df["month_word"].unique()
            selected_month = st.multiselect("Select a month", options=unique_months)
            if not selected_month:
                df = df
            else:
                df = df[df["month_word"].isin(selected_month)]

        # Filter data based on year and month
        if on:
            unique_campaign = df["name"].unique()
            selected_campaign = st.selectbox("Select a campaign", unique_campaign)
            df = df[df["name"] == selected_campaign]

    # Calculate metrics
    emails_sent = df["target_count"].sum()
    emails_open = df["open"].sum()
    emails_click = df["click"].sum()
    emails_submitted = df["submitted"].sum()
    emails_reported = df["reported"].sum()
    emails_pdf = df["downloaded_attachement"].sum()

    open_rate, click_rate, data_submitted, nb_reports, emails_download = (
        calculate_click_rate(
            emails_click,
            emails_open,
            emails_sent,
            emails_submitted,
            emails_reported,
            emails_pdf,
        )
    )

    # Overview
    if on:
        st.title(f"Campaign details: {selected_campaign}")
    else:
        st.title("General overview")

    # Display pie charts for metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### Open rate")
        pie_chart(open_rate)

    with col2:
        st.markdown("#### Click rate")
        pie_chart(click_rate)

    with col3:
        st.markdown("#### Data submitted")
        pie_chart(data_submitted)

    with col4:
        st.markdown("#### Downloads")
        pie_chart(emails_download)

    # Display bar charts for the campaign view
    if on:

        def addlabels(values: list[float]) -> None:
            """
            Place a text label above each bar with its value
            Adjust the height of the label slightly above the bar using 0.01 * max(values)
            """
            for i, value in enumerate(values):
                plt.text(
                    i, value + 0.01 * max(values), str(value), ha="center", fontsize=8
                )  # Adjust 0.05 to change the distance

        st.markdown("### Campaign details")
        plt.rcParams.update({"font.size": 8})
        categories = [
            "Sent",
            "Opened",
            "Clicked",
            "PDF downloads",
            "Data submitted",
            "Reported",
        ]
        values = [
            emails_sent,
            emails_open,
            emails_click,
            emails_pdf,
            emails_submitted,
            emails_reported,
        ]
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(
            categories,
            values,
            color=["#5C2D91", "#754db8", "#AD96C8", "#DE2A56", "#6F142B", "#C0C1C4"],
        )
        plt.xticks(rotation=45)
        ax.set_ylabel("How many people", fontsize=10)
        addlabels(values)
        st.pyplot(fig)

    # Display histogram for the general view
    else:
        if years == None:
            st.markdown("### Overview of the lasts campaigns")
            current_date = datetime.datetime.now()
            one_year_ago = current_date - pd.DateOffset(months=12)
            df = df[df["created_at"] >= one_year_ago]
        else:
            st.markdown(f"### Overview of the campaigns in {years}")
            df = df[df["year"] == years]

        df_last_10 = df.tail(10)
        x_labels = df_last_10["created_at"]
        x_index = range(len(df_last_10))
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x_index, df_last_10["open"], label="Opens", color="#5C2D91", marker="o")
        ax.plot(
            x_index, df_last_10["click"], label="Clicks", color="#AD96C8", marker="o"
        )
        ax.plot(
            x_index,
            df_last_10["submitted"],
            label="Data submitted",
            color="#DE2A56",
            marker="o",
        )
        ax.plot(
            x_index,
            df_last_10["downloaded_attachement"],
            label="PDF downloads",
            color="#6F142B",
            marker="o",
        )
        ax.plot(
            x_index,
            df_last_10["reported"],
            label="Reports",
            color="#C0C1C4",
            marker="o",
        )
        ax.set_ylabel("Number of events")
        ax.legend()
        ax.set_xticks(x_index)
        ax.set_xticklabels(x_labels, rotation=45)
        st.pyplot(fig)

    plt.clf()

    # Dataframe view
    if on:
        st.markdown(f"### Detailed data view - {selected_campaign}")
    else:
        st.markdown("### Detailed data view - last 20 campaigns")
    short_df = df.drop(
        ["status", "month", "year", "day", "month_word", "date", "id"], axis=1
    )
    short_df.sort_values(by="created_at", ascending=False, inplace=True)
    st.dataframe(short_df.head(20))

    # Events dataframe
    if on:
        st.markdown(f"### Events overview - {selected_campaign}")
        events_filtered = events[events["campaign_name"] == selected_campaign]
        st.dataframe(events_filtered)


graphs(merged_df, events_df)
