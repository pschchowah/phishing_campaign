# **phishing_campaign**

![Phish & Clicks.]([https://www.shutterstock.com/image-vector/seamless-border-cute-retro-houses-600nw-1111423082.jpg](https://discord.com/channels/708408549704990732/1289222632973013095/1331993762825502771))

[Introduction](#Introduction)     |     [Description](#Description)       |       [Usage](#Usage)    |     [Timeline](#Timeline)       |       [List of Improvements](#list-of-improvements)    |    [Contributors](#contributors)

## **Introduction**
Phish & Clicks is a web-based application built with FastAPI and Streamlit that enables security teams to:
- Launch targeted phishing simulation campaigns
- Track employee interactions with phishing emails
- Analyze campaign effectiveness through detailed metrics
- Provide instant security awareness training

## **Description**

Packages used:
- `fastapi`: Backend API framework
- `streamlit`: Frontend dashboard interface
- `sqlalchemy`: Database ORM
- `pandas`: Data manipulation and analysis
- `numpy` : ???
- `matplotlib`: Data visualization
- `pydantic`: Data validation
- `jinja2`: HTML template rendering
- `psycopg2`: PostgreSQL adapter


## **Usage**
1. Install dependencies
   pip install -r requirements.txt

2. Start the Streamlit dashboard
   streamlit run app/app.py

3. Login with credentials
   from secrets.toml

4. Create Campaign
  - Navigate to "Campaign Launch"
  - Enter campaign details
  - Upload target CSV file (required columns: First Name, Last Name, Email)
  - Select phishing template options
  - Launch campaign 


## **Timeline**
20 Jan 2025 - project phase initiated at BeCode Brussels AI & Data Science Bootcamp

24 Jan 2025 - project ended


## **List of Improvements**
- Scoring System
- Email scheduling system
- Add more phishing templates
- Add ability to input employee data from an external database
- Add user security permissions for accessibility to application

## **Contributors**
- Data Analysts:

  David Anselot

  Thérèse de Backer

  Nicole Pretorius

  Patrycja Schaefer
  
- Data Engineers:
  
  Edoardo Lai

  Tumi Modiba

  Miro Fronhoffs
