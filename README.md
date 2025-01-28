# **Phishing Simulation Platform**

[![phish-n-clicks-logo-hori-purple.png](https://i.postimg.cc/dQSDc9yr/phish-n-clicks-logo-hori-purple.png)](https://postimg.cc/yWc7Fcn8)


[Introduction](#Introduction)     | [Features](#Features)     | [Requirements](#Requirements)     |     [Installation](#Installation)       |       [Usage](#Usage)    |     [Project Timeline](#project-timeline)         |    [Contributors](#contributors)     |       [Future Improvements](#future-improvements)    |      [Disclaimer](#disclaimer)

## **Introduction**

Phish & Clicks is a web-based application built with FastAPI 
and Streamlit that enables security teams to:
- Launch targeted phishing simulation campaigns
- Track employee interactions with phishing emails
- Analyze campaign effectiveness through detailed metrics
- Provide instant security awareness training

## **Features**

- **Phishing Email Simulation**: Tools to create and send simulated phishing emails to target users.
- **Campaign Analytics**: Analyze the response rates, click-through rates, and other metrics from simulated campaigns (note that in order to track response rates, a tracking service was deployed from a separate repository. You can find more details [here](https://github.com/Dadelidodu/phishing_campaign_api_deploy)).
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

2. Log in with the secrets.toml username and password you just defined

3. Campaign Launch :

    - Campaign Name is mandatory
    - Use the dataset template provided in the 'data' folder for upload

4. Navigate through pages for Overview : 
    
    - Data Overview
    - Campaign Metrics

## **Project Timeline**

13 Jan 2025 - project phase initiated at BeCode Brussels AI & Data Science Bootcamp

24 Jan 2025 - project ended


## **Contributors**

   David Anselot  [github](https://github.com/Dadelidodu) [LinkedIn](https://www.linkedin.com/in/david-a-486841214/)

   Thérèse de Backer [github](https://github.com/therese-debacker) <a href="https://www.linkedin.com/in/th%C3%A9r%C3%A8se-de-backer-8963735a/">LinkedIn</a>

   Nicole Pretorius [github](https://github.com/npret) [LinkedIn](https://www.linkedin.com/in/nicolepret/)

   Patrycja Schaefer  [github](https://github.com/pschchowah) [LinkedIn](https://www.linkedin.com/in/patrycjaschaefer/)
  
   Edoardo Lai   [github](https://github.com/edoardolai) [LinkedIn](https://www.linkedin.com/in/edoardo-lai/)

   Tumi Modiba [github](https://github.com/2moonyo)  [LinkedIn](https://www.linkedin.com/in/tumi-modiba-3023b326/)

   Miro Fronhoffs [github](https://github.com/MiroFronhoffs) [LinkedIn](www.linkedin.com/in/miro-fronhoffs-263661219)


## **Future Improvements**
### General
- Scoring System
- Email scheduling system
- Add more phishing templates
- Add ability to input employee data from an external database
- Add user security permissions for accessibility to application
### Template Management
- Add customizable email templates with HTML/CSS support
- Template categorization and tagging system
- Preview functionality for templates
- Import/export template capabilities
### API Enhancement
- Implement API keys for frontend authentication
- Separate data access per front-end instance
### Security & Access Control
- User authentication system with role-based access control
- Implement the following roles:
  - Campaign Manager (full access)
  - Campaign Viewer (read-only access)
  - Template Editor (template management only)
  - Report Analyst (analytics access only)

## Disclaimer

This tool is for educational purposes only. Misuse of this project for malicious activities is strictly prohibited.

 
