import requests
from typing import Dict, List, Optional, Any


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_events(self, campaign_id: Optional[int] = None,employee_id: Optional[int] = None) -> List[Dict]:
        """Get events, optionally filtered by campaign"""
        try:
            params = {}
            if campaign_id:
                params["campaign_id"] = campaign_id
            #if employee_id:
                #params["employee_id"] = employee_id
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

    def add_employee(self, employee_data: Dict[str, Any]) -> Dict:
        """
        Add an employee to database 
        """
        try:
            if not employee_data.get("email"):
                raise ValueError("Email is required"
                )
             # Debug print of request data    
            print(f"Sending employee data: {employee_data}")
            

            response = requests.post(
                f"{self.base_url}/employees",
                json=employee_data
            )
            # Print detailed error response
            if not response.ok:
                print(f"Response status: {response.status_code}")
                print(f"Response headers: {response.headers}")
                print(f"Response text: {response.text}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error adding employee: {str(e)}")
            print(f"Request body: {employee_data}")
            print(f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}")
            raise
    
    def get_employees(self) -> List[Dict]:
        """Get all employees"""
        try:
            response = requests.get(f"{self.base_url}/employees")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching employees: {str(e)}")
            print(
                f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}"
            )
            raise