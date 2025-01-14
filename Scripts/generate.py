import google.generativeai as genai
import json
import os
import requests
import pandas as pd


class Generator:

    def __init__(self, api_key=None, model=None):

        self.api_key = api_key

        if api_key == None:
            self.get_api_key()

    def get_api_key(self):
        
        config_file = "data/config.json"

        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config = json.load(file)
                self.api_key = config.get("GEMINI_API_KEY")
            print("Configuration loaded successfully.")
        else:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

    def connect(self):

        genai.configure(api_key=self.api_key)

    def initialize_model(self):

        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_text(self, prompt=None):

        self.prompt = prompt
        response = self.model.generate_content(self.prompt)

        if prompt != None:
            print("Prompt: ",self.prompt)
            print("Output: ")
            print(response.text)
        else:
            print("Please provide a prompt to generate text.")
    
    def fetch_data(self):

        url = "http://your-fastapi-endpoint/data"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df.to_csv("data/fetched_data.csv", index=False)
            print("Data fetched and saved successfully.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

