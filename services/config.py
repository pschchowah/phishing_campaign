import os
import json
import google.generativeai as genai


class Configurator:
    """
    The Configurator class manages the setup and initialization of a generative AI model.
    It handles API key retrieval, configuration, and model initialization.

    Attributes:
        api_key (str): The API key for accessing the generative AI service.
        model_name (str): The name of the generative AI model to be used.
        model (object): The generative AI model instance, initialized during runtime.
    """

    def __init__(self, api_key=None, model_name="gemini-pro"):
        """
        Initialize the Configurator class.

        Args:
            api_key (str, optional): The API key for the generative AI service. Defaults to None.
            model_name (str, optional): The name of the model to use. Defaults to "gemini-pro".
        """
        self.api_key = api_key
        self.model_name = model_name
        self.model = None

        if not self.api_key:
            self.get_api_key()

    def get_api_key(self):
        """
        Retrieve the API key from a configuration file.

        The method checks if the config file exists
        and reads the API key from it.
        Raises:
            FileNotFoundError: If the config file does not exist.
            ValueError: If the API key is missing from the config file.
        """

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
        """
        Configure the API using the retrieved API key.

        Raises:
            ValueError: If the API key is missing.
        """
        if not self.api_key:
            raise ValueError("API key is missing.")
        genai.configure(api_key=self.api_key)
        print("API configured successfully.")

    def initialize_model(self):
        """
        Initialize the generative AI model.

        This method creates an instance of the model using
        the provided model name.
        Raises:
            ValueError: If the model name is missing.
        """

        if not self.model_name:
            raise ValueError("Model name is missing.")
        self.model = genai.GenerativeModel(self.model_name)
        print(f"Model '{self.model_name}' initialized successfully.")
