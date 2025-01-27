# **phishing_campaign**

![Phish & Clicks.]([https://www.shutterstock.com/image-vector/seamless-border-cute-retro-houses-600nw-1111423082.jpg])

[Introduction](#Introduction)     |     [Description](#Description)       |       [Usage](#Usage)    |     [Timeline](#Timeline)       |       [List of Improvements](#list-of-improvements)    |    [Contributors](#contributors)

## **Introduction**

Overview

The Phishing Campaign Simulator is a project designed to simulate and analyze phishing campaigns for educational and research purposes. This tool can help individuals and organizations understand how phishing attempts work and identify ways to mitigate risks. It also provides insights into phishing techniques and their effectiveness in compromising targets.

Features

Simulation of Phishing Campaigns: Generate custom phishing scenarios to test user behavior.
Dataset Integration: Use real-world datasets to analyze trends in phishing campaigns.
Data Analysis Tools: Leverage Python libraries like pandas, numpy, and matplotlib to analyze results.
Customization Options: Create tailored phishing emails and schedules for testing purposes.

## **Description**

Packages used:
- pandas
- numpy
- matplotlib
- ???


## **Usage**
Prerequisites

Ensure you have the following installed:

Python 3.8 or later
Required Python packages (install via requirements.txt)

Installation

Clone this repository:

git clone https://github.com/pschchowah/phishing_campaign.git
cd phishing_campaign

Install dependencies:

pip install -r requirements.txt

Add your datasets (if applicable) to the project directory.

Usage
Run the main script:

bash
Copy
Edit
python main.py
Configure the phishing campaign parameters as prompted or as specified in the configuration file.

Review generated reports and visualizations.

Project Structure

bash
Copy
Edit
phishing_campaign/
├── datasets/          # Datasets for analysis (add your files here)
├── scripts/           # Core Python scripts
├── requirements.txt   # Dependency list
├── README.md          # Project documentation
└── LICENSE            # License information


## **Timeline**
20 Jan 2025 - project phase initiated at BeCode Brussels AI & Data Science Bootcamp

24 Jan 2025 - project ended


## **List of Improvements**
- Scoring System
- Scheduling
- ???

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

## Future Improvements
### Template Management
- Add customizable email templates with HTML/CSS support
- Template categorization and tagging system
- Preview functionality for templates
- Import/export template capabilities
### API Enhancement
- Implement API keys for frontend authentication
- Separate data access per frontend instance
### Security & Access Control
- User authentication system with role-based access control
- Implement the following roles:
  - Campaign Manager (full access)
  - Campaign Viewer (read-only access)
  - Template Editor (template management only)
  - Report Analyst (analytics access only)
##Disclaimer

This tool is for educational purposes only. Misuse of this project for malicious activities is strictly prohibited.

 
