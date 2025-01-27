# **phishing_campaign**

![Phish & Clicks.]([https://www.shutterstock.com/image-vector/seamless-border-cute-retro-houses-600nw-1111423082.jpg](https://discord.com/channels/708408549704990732/1289222632973013095/1331993762825502771))

[Introduction](#Introduction)     |     [Description](#Description)       |       [Usage](#Usage)    |     [Timeline](#Timeline)       |       [List of Improvements](#list-of-improvements)    |    [Contributors](#contributors)

## **Features**

- **Phishing Email Simulation**: Tools to create and send simulated phishing emails to target users.
- **Campaign Analytics**: Analyze the response rates, click-through rates, and other metrics from simulated campaigns.
- **Customizable Templates**: Predefined email templates and options to create custom phishing templates.
- **Educational Tools**: Resources for educating users about phishing and how to recognize malicious emails.
- **Data Visualization**: Graphs and charts to visualize the impact and effectiveness of campaigns.

## **Requirements**

To run this toolkit, ensure you have the following installed:

- Python 3.8 or later
- Required Python libraries (listed in `requirements.txt`)

## **Installation**

1. Clone this repository:
```bash
   git clone https://github.com/pschchowah/phishing_campaign.git
   cd phishing_campaign
```

2. Install the dependencies:
```bash
    pip install -r requirements.txt
```

3. Collect your credentials from Google Cloud Console and add it to 'credentials' folder :
```bash
    
    ## add config.json : containing Gemini API_Key like this

    {"GEMINI_API_KEY": "XXXXXXXXXXXXXXXXXXXXXXXXX"}


    ## add gmail_credentials.json : containing Gmail API gmail_credentials like this

    {
        "installed":{"client_id":"xxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com",
        "project_id":"xxxxxxxxxxxxxxxxxxxxxx",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "redirect_uris":["http://localhost"]
        }
    }
```
4. Create a secrets.toml file and add it to '.streamlit' folder:
```bash
    ["authentication"]
    "username" = "yourusername"
    "password" = "yourpassword"
```

## **Usage**

1. Run this command on local for testing : *streamlit run app/app.py*

2. login with the secrets.toml username and password you just defined

3. Campaign Launch :

    - Campaign Name is mandatory
    - use dataset template provided in 'data' folder for upload

4. Navigate through pages for Overview : 
    
    - Data Overview
    - Campaign Metrics

## **Timeline**

20 Jan 2025 - project phase initiated at BeCode Brussels AI & Data Science Bootcamp

24 Jan 2025 - project ended


## **List of Improvements**

- Scoring System
- Scheduling
- Database linking for new targets input


## **Contributors**

  David Anselot

  Thérèse de Backer

  Nicole Pretorius

  Patrycja Schaefer
  
  Edoardo Lai

  Tumi Modiba

  Miro Fronhoffs
