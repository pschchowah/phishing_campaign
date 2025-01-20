import os
import json
import google.generativeai as genai


class Configurator:

    def __init__(self, api_key=None, model_name="gemini-pro"):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None

        if not self.api_key:
            self.get_api_key()

    def get_api_key(self):
        config_file = "credentials/config.json"

        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config = json.load(file)
                self.api_key = config.get("GEMINI_API_KEY")
                if not self.api_key:
                    raise ValueError("GEMINI_API_KEY is missing in the config file.")
            print("Configuration loaded successfully.")
        else:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

    def connect(self):
        if not self.api_key:
            raise ValueError("API key is missing.")
        genai.configure(api_key=self.api_key)
        print("API configured successfully.")

    def initialize_model(self):
        if not self.model_name:
            raise ValueError("Model name is missing.")
        self.model = genai.GenerativeModel(self.model_name)
        print(f"Model '{self.model_name}' initialized successfully.")