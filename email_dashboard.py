import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# class CampaignReport:
#     def __init__(self, id):
#         self.id = id
#         self.summary = api.campaigns.summary(campaign_id=self.id)
#         self.created_date = self.summary.created_date
#         self.launch_date = self.summary.launch_date
#         self.send_by_date = self.summary.send_by_date
#         self.completed_date = self.summary.completed_date
#         self.status = self.summary.status
#         self.name = self.summary.name
#         self.stats = self.summary.stats
#         self.total = self.stats.total
#         self.sent = self.stats.sent
#         self.opened = self.stats.opened
#         self.clicked = self.stats.clicked
#         self.submitted_data = self.stats.submitted_data
#         # self.email_reported = self.stats.email_reported
#         self.error = self.stats.error

#     def general_data(self):
#         print("summary: ", self.opened)
#         print(self.created_date)

#     def list_data(self):
#         campaign_data = [self.created_date,self.launch_date, self.send_by_date, self.completed_date, self.status, 
#                          self.name, self.total, self.sent, self.opened, self.clicked, self.error]
#         return campaign_data

# class CampaignsDashboard:
#     def __init__(self, id):
#         self.df = pd.Dataframe()

#     def df_campaign(self, campaign_list):
#         self.df.loc[len(self.df)] = campaign_list
#         return self.df
#     # def display_data(self):
#     # Loading CSS style
#         # st.markdown(
#         #     "<style>" + open("style.css").read() + "</style>", unsafe_allow_html=True)

# id_campaign = 11
# campaign1 = CampaignReport(id_campaign)

# Test dataframe
data = {'campaign id': [1,2,3,4,5],
        'campaign name': ['Webinar Email','Password Reset Email','Service Upgrade Email 1','Account Verification Email','Service Upgrade Email 2'],
        'subject': ['webinar','password reset','service upgrade','account verification','service upgrade'],
        'sent date' : ['12/01','14/02','10/03','13/04','17/05'],
        'year' : [2024, 2025, 2025, 2025, 2025],
        'month' : ['January', 'Februari', 'March', 'April', 'May'],
        'number of sent emails': [200,200,200,200,200],
        'number of delivered emails': [199,200,198,199,200],
        'number of opens': [34,54,23,32,21],
        'number of clicks': [16,5,23,12,3]
        }

# Create DataFrame
df = pd.DataFrame(data)

# functions
def pie_chart(label, data):
    colors = ['#7d57a7','#e6e6e7']
    # fig1, ax1 = plt.subplots()
    plt.pie(data, colors = colors, labels=label, autopct='%1.1f%%', startangle=90)
    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.clf()

# start streamlit page
# st.set_page_config(
#     page_title="Phishing Email Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded")
    
def calculate_click_rate(campaign_clicks, campaign_opens, campaign_delievered, campaign_sent):
    click_rate  = campaign_clicks/campaign_sent*100 
    open_rate  = campaign_opens/campaign_sent*100
    click_open  = campaign_clicks/campaign_opens*100 
    delivered_rate  = campaign_delievered/campaign_sent*100
    return open_rate, click_rate, click_open, delivered_rate

# sidebar
with st.sidebar:
    st.title('Phishing Email Dashboard')
    on = st.toggle("Per campaign", value=False)

    if on:
        selected_campaign = st.selectbox('Select a campaign', df["campaign name"])
        df = df[df["campaign name"] == selected_campaign]
    else:
        unique_years = df['year'].unique()
        years = st.segmented_control('Which year', options=unique_years)
        if years == None:
            df = df
        else:
            df = df[df['year'] == years]
            unique_months = df['month'].unique()
            selected_month = st.multiselect('Select a month', options=unique_months)
            if not selected_month:
                df = df
            else:
                df = df[df["month"].isin(selected_month)]

emails_sent_df = df['number of sent emails'].sum()
emails_delivered_df = df['number of delivered emails'].sum()
emails_open_df = df['number of opens'].sum()
emails_click_df = df['number of clicks'].sum()

open_rate_df, click_rate_df, click_open_df, delivered_rate_df = calculate_click_rate(emails_click_df, emails_open_df, emails_delivered_df, emails_sent_df)

if on:
    st.title('Campaign details: {selected_campaign}')
else:
    st.title('General overview')

# general data
per1, per2, per3, per4 = st.columns(4)

with per1:
    st.subheader("Open rate")
    # Pie chart
    labels_clicks = ['Clicked', 'No clicks']
    percentage_open = [open_rate_df, 100-open_rate_df]
    pie_chart(labels_clicks, percentage_open)

with per2:
    st.subheader("Click rate")
    # Pie chart
    labels_clicks = ['Clicked', 'No clicks']
    percentage_clicks = [click_rate_df, 100-click_rate_df]
    pie_chart(labels_clicks, percentage_clicks)

with per3:
    st.subheader("Click to open")
    # Pie chart
    labels_clicks = ['Clicked', 'No clicks']
    percentage_click_open = [click_open_df, 100-click_open_df]
    pie_chart(labels_clicks, percentage_click_open)

with per4:
    st.subheader("Delivered")
    # Pie chart
    labels_clicks = ['Clicked', 'No clicks']
    percentage_delivered = [delivered_rate_df, 100-delivered_rate_df]
    pie_chart(labels_clicks, percentage_delivered)   


# columns charts
fig1, fig2 = st.columns(2)
with fig1:
    st.markdown("### Campaign details")

    # Données pour le graphique
    categories = ['Sent', 'Open', 'Click']
    values = [emails_sent_df, emails_open_df, emails_click_df]

    # Création du graphique à barres
    fig, ax = plt.subplots()
    ax.bar(categories, values, color=['#5C2D91', '#7d57a7', '#DE2A56'])

    # Ajout des labels et titre
    ax.set_ylabel('Number of Emails')
    # ax.set_title(f'Performance of {selected_campaign}')

    # Affichage du graphique dans Streamlit
    st.pyplot(fig)

plt.clf()

with fig2:
    st.markdown("### Percentage of clicks per business units")
    business_units = ['Proximus','Proximus Billing Service','Proximus Ada']
    percentage_clicking = [14, 17, 7]
    plt.bar(business_units, percentage_clicking, color='#7d57a7')
    plt.xlabel('Business units')
    plt.ylabel('Percentage of clicking')
    st.pyplot(plt)


# dataframe view
st.markdown("### Detailed Data View")
st.dataframe(df)



# list of people who clicked
# check emails when people got phished and see if it can be reused for other people (maybe it's a better phishing email)
# lists of who clicks, who reported it?
# percentage of opens/clicks per person --> show people who clicks the most
# list of people who clicked more than in 50% of emails 
# if they clicked --> landing page : how to recognze a phishing email and recommendation links
# filter par date range of emails sent + specific campaign
# + after 3 following emails clicked --> automatic emails: you click in x phishing email : take the training 
# filter people who clicked on the last x emails
# did people click/open the training email