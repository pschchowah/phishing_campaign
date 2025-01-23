import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
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
    tracking_data = api_client.get_events()
    return pd.DataFrame(tracking_data)

events_df = dataframe_creation()

all_event_types = ["open", "click", "submitted", "downloaded_attachement","reported"]
event_counts = events_df.groupby(["campaign_id", "event_type"]).size().unstack(fill_value=0)

for event in all_event_types:
    if event not in event_counts.columns:
        event_counts[event] = 0

# Establish a connection with the database
engine = create_engine("sqlite:///./phishing_campaigns.db")
 
# Read the sqlite table
campaigns_df = pd.read_sql_table(
    "campaigns",
    con=engine
)
 
# Create final dataFrame
merged_df = pd.merge(campaigns_df, event_counts, left_on="id", right_on="campaign_id", how="left")
merged_df = merged_df.fillna(0)

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

def calculate_click_rate(
    campaign_clicks, campaign_opens, campaign_sent, campaign_submitted, campaign_reports, campaign_download
):
    click_rate = round(campaign_clicks / campaign_sent * 100, 2)
    open_rate = round(campaign_opens / campaign_sent * 100, 2)
    data_submitted = round(campaign_submitted / campaign_sent * 100, 2)
    reports = round(campaign_reports / campaign_sent * 100, 2)
    downloads = round(campaign_download / campaign_sent * 100, 2)
    return open_rate, click_rate, data_submitted, reports, downloads

def graphs(df):
    # Time data
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['month'] = df['created_at'].dt.strftime('%B')
    df['year'] = df['created_at'].dt.year
    df['day'] = df['created_at'].dt.day

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
            unique_months = df["month"].unique()
            selected_month = st.multiselect("Select a month", options=unique_months)
            if not selected_month:
                df = df
            else:
                df = df[df["month"].isin(selected_month)]
        if on:
            unique_campaign = df["name"].unique()
            selected_campaign = st.selectbox("Select a campaign", unique_campaign)
            df = df[df["name"] == selected_campaign]
            

    # COMMENT AVOIR LES SENT
    # emails_sent_df = df["sent"].sum() # HOW ????
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
        st.markdown("### Campaign details")
        categories = ["Sent", "Opens", "Click", "PDF downloads", "Data submitted", "Reported"]
        values = [emails_sent, emails_open, emails_click, emails_pdf, emails_submitted, emails_reported]
        fig, ax = plt.subplots()
        ax.bar(categories, values, color=["#5C2D91", "#7d57a7", "#DE2A56"])
        ax.set_ylabel("Number of Emails")
        st.pyplot(fig)
    else:
        st.markdown("### Overview of the lasts campaigns")
        if years == None:
            current_date = datetime.datetime.now()  
            one_year_ago = current_date - pd.DateOffset(months=12) 
            df = df[df['created_at'] >= one_year_ago]
        else:
            df = df[df["year"] == years]
        
        fig, ax = plt.subplots(figsize=(10, 6)) 
        ax.plot(df['created_at'], df['click'], label="Clicks", color="#7d57a7", marker='o')
        ax.plot(df['created_at'], df['open'], label="Opens", color="#5C2D91", marker='o')
        ax.plot(df['created_at'], df['reported'], label="Reports", color="#DE2A56", marker='o')
        ax.plot(df['created_at'], df['submitted'], label="Submitted", color="#28A745", marker='o')
        ax.plot(df['created_at'], df['downloaded_attachement'], label="Downloads", color="#28A745", marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of events")
        ax.set_title("Evolution over time")
        ax.legend()
        st.pyplot(fig)

    plt.clf()

# #         # RAJOUTER reports & data submitted
# #         st.markdown("### Overview per business units")
# #         # business_units = ["Proximus", "Proximus Billing Service", "Proximus Ada"]
# #         # percentage_clicking = [14, 17, 7]
# #         # plt.bar(business_units, percentage_clicking, color="#7d57a7")
# #         # plt.xlabel("Business units")
# #         # plt.ylabel("Percentage of clicking")
# #         # st.pyplot(plt)
# #         business_units = ["Proximus", "Proximus Billing Service", "Proximus Ada"]
# #         percentage_clicking = [14, 17, 7]  # Pourcentage de clics
# #         percentage_submitted = [9, 12, 5]  # Pourcentage de soumissions
# #         percentage_reports = [3, 4, 1]    # Pourcentage de signalements

# #         # Création du graphique
# #         fig, ax = plt.subplots()

# #         # Tracer les barres pour chaque catégorie
# #         bar_width = 0.25
# #         index = range(len(business_units))

# #         # Barres pour les clics, soumissions et signalements
# #         ax.bar(index, percentage_clicking, bar_width, label="Click rate", color="#7d57a7")
# #         ax.bar([i + bar_width for i in index], percentage_submitted, bar_width, label="Submitted rate", color="#5C2D91")
# #         ax.bar([i + bar_width * 2 for i in index], percentage_reports, bar_width, label="Report rate", color="#DE2A56")

# #         # Ajouter des labels et un titre
# #         ax.set_xlabel("Business units")
# #         ax.set_ylabel("Percentage (%)")
# #         # ax.set_title("Comparison of Clicks, Submitted, and Reports by Business Unit")
# #         ax.set_xticks([i + bar_width for i in index])  # Positionner les étiquettes au centre des groupes de barres
# #         ax.set_xticklabels(business_units)
# #         ax.legend()

# #         # Affichage du graphique avec Streamlit
# #         st.pyplot(fig)

    # dataframe view
    if on:
        st.markdown(f"### Detailed data view - {selected_campaign}")
    else:
        st.markdown("### Detailed data view - last 20 campaigns")
    short_df = df.drop(['status', 'month', 'year', 'day'], axis=1)
    short_df.sort_values(by='created_at', ascending = False, inplace = True) 
    st.dataframe(short_df.head(20))

graphs(merged_df)