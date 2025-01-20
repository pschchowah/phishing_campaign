import requests
from typing import Dict, List, Optional


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_events(self, campaign_id: Optional[int] = None) -> List[Dict]:
        """Get events, optionally filtered by campaign"""
        try:
            params = {"campaign_id": campaign_id} if campaign_id else {}
            response = requests.get(f"{self.base_url}/events", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events: {str(e)}")
            print(
                f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}"
            )
            raise

    def create_campaign(self, name: str, description: str = "") -> Dict:
        """Create a new campaign"""
        try:
            data = {"name": name, "description": description}
            response = requests.post(f"{self.base_url}/campaigns", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating campaign: {str(e)}")
            print(
                f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}"
            )
            raise

    def get_campaigns(self) -> List[Dict]:
        """Get all campaigns"""
        try:
            response = requests.get(f"{self.base_url}/campaigns")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching campaigns: {str(e)}")
            print(
                f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}"
            )
            raise

    def get_campaign(self, campaign_id: int) -> Dict:
        """Get a specific campaign details"""
        try:
            response = requests.get(f"{self.base_url}/campaigns/{campaign_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching campaign: {str(e)}")
            print(
                f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}"
            )
            raise

    def update_campaign_status(self, campaign_id: int, status: str) -> Dict:
        """Update campaign status"""
        try:
            response = requests.patch(
                f"{self.base_url}/campaigns/{campaign_id}/status",
                json={"status": status},
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating campaign status: {str(e)}")
            print(
                f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}"
            )
            raise
