import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import datetime
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))
from api_client import APIClient

# Event dataframe
def dataframe_creation():
    # Fetch data from external endpoint
    api_client = APIClient()
    tracking_data_events = api_client.get_events()
    tracking_data_campaigns = api_client.get_campaigns()
    return pd.DataFrame(tracking_data_events), pd.DataFrame(tracking_data_campaigns)

events_df, campaigns_df = dataframe_creation()

def create_final_dataframe(events_df,campaigns_df):
    all_event_types = ["open", "click", "submitted", "downloaded_attachement","reported"]
    event_counts = events_df.groupby(["campaign_id", "event_type"]).size().unstack(fill_value=0)
    for event in all_event_types:
        if event not in event_counts.columns:
            event_counts[event] = 0
 
    # Create final dataFrame
    df = pd.merge(campaigns_df, event_counts, left_on="id", right_on="campaign_id", how="left")
    df = df.fillna(0)
    return df

merged_df = create_final_dataframe(events_df, campaigns_df)

# Pie charts
def pie_chart(data):
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

# Percentage calculations
def calculate_click_rate(
    campaign_clicks, campaign_opens, campaign_sent, campaign_submitted, campaign_reports, campaign_download
):
    click_rate = round(campaign_clicks / campaign_sent * 100, 2)
    open_rate = round(campaign_opens / campaign_sent * 100, 2)
    data_submitted = round(campaign_submitted / campaign_sent * 100, 2)
    reports = round(campaign_reports / campaign_sent * 100, 2)
    downloads = round(campaign_download / campaign_sent * 100, 2)
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

# Creation of the dashboard on Streamlit
def graphs(df, events):
    # Time data
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['month_word'] = df['created_at'].dt.strftime('%B')
    df['year'] = df['created_at'].dt.year
    df['day'] = df['created_at'].dt.day
    df['month'] = df['created_at'].dt.month
    df['date'] = pd.to_datetime(df[['day', 'month', 'year']])

    # Sidebar
    with st.sidebar:
        st.title("Phishing Email Dashboard")
        on = st.toggle("Per campaign", value=False)
        unique_years = df["year"].unique()
        years = st.segmented_control("Which year", options=unique_years)
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
        if on:
            unique_campaign = df["name"].unique()
            selected_campaign = st.selectbox("Select a campaign", unique_campaign)
            df = df[df["name"] == selected_campaign]
            

    # Campaigns data
    emails_sent = df['target_count'].sum()
    emails_open = df['open'].sum()
    emails_click = df['click'].sum()
    emails_submitted = df['submitted'].sum()  
    emails_reported = df['reported'].sum()
    emails_pdf = df['downloaded_attachement'].sum() 


    open_rate, click_rate, data_submitted, nb_reports, emails_download = calculate_click_rate(
        emails_click, emails_open, emails_sent, emails_submitted, emails_reported, emails_pdf
    )

    # Overview
    if on:
        st.title(f"Campaign details: {selected_campaign}")
    else:
        st.title("General overview")

    # Pie charts
    col1,col2,col3,col4 = st.columns(4)

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
    
    # Bar charts
    if on:
        def addlabels(values):
            for i, value in enumerate(values):
                plt.text(i, value + 0.01*max(values), str(value), ha='center', fontsize=8)  # Adjust 0.05 to change the distance

        st.markdown("### Campaign details")
        plt.rcParams.update({'font.size': 8})
        categories = ["Sent", "Opened", "Clicked", "PDF downloads", "Data submitted", "Reported"]
        values = [emails_sent, emails_open, emails_click, emails_pdf, emails_submitted, emails_reported]
        fig, ax = plt.subplots()
        ax.bar(categories, values, color=["#5C2D91", "#754db8", "#AD96C8", "#DE2A56", "#6F142B", "#C0C1C4"])
        plt.xticks(rotation=45)
        ax.set_ylabel("How many people", fontsize=10)
        addlabels(values)

        st.pyplot(fig)
    else:
        if years == None:
            st.markdown("### Overview of the lasts campaigns")
            current_date = datetime.datetime.now()  
            one_year_ago = current_date - pd.DateOffset(months=12) 
            df = df[df['created_at'] >= one_year_ago]
        else:
            st.markdown(f"### Overview of the campaigns in {years}")
            df = df[df["year"] == years]
        
        df_last_10 = df.tail(20)
        fig, ax = plt.subplots(figsize=(10, 6)) 
        ax.plot(df_last_10['date'], df_last_10['open'], label="Opens", color="#5C2D91", marker='o')
        ax.plot(df_last_10['date'], df_last_10['click'], label="Clicks", color="#AD96C8", marker='o')
        ax.plot(df_last_10['date'], df_last_10['submitted'], label="Data submitted", color="#DE2A56", marker='o')
        ax.plot(df_last_10['date'], df_last_10['downloaded_attachement'], label="PDF downloads", color="#6F142B", marker='o')
        ax.plot(df_last_10['date'], df_last_10['reported'], label="Reports", color="#C0C1C4", marker='o')
        ax.set_ylabel("Number of events")
        ax.legend()
        st.pyplot(fig)

    plt.clf()

    # Dataframe view
    if on:
        st.markdown(f"### Detailed data view - {selected_campaign}")
    else:
        st.markdown("### Detailed data view - last 20 campaigns")
    short_df = df.drop(['status', 'month', 'year', 'day', 'month_word', 'date', 'id'], axis=1)
    short_df.sort_values(by='created_at', ascending = False, inplace = True) 
    st.dataframe(short_df.head(20))

    # Events dataframe
    if on:
        st.markdown(f"### Events overview - {selected_campaign}")
        events_filtered = events[events["campaign_name"] == selected_campaign]
        st.dataframe(events_filtered)

graphs(merged_df, events_df)