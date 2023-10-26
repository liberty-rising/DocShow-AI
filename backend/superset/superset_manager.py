import requests
from typing import Optional

class SupersetManager:
    def __init__(self):
        self.base_url = "http://superset:8088/api/v1"
        self.auth_url = f"{self.base_url}/security/login"
        self.headers = None  # To store the Authorization header
    
    def authenticate_superset(self):
        payload = {
            "username": "admin",
            "password": "admin",
            "provider": "db"
        }
    
        response = requests.post(self.auth_url, json=payload)

        if response.status_code == 200:
            auth_info = response.json()
            access_token = auth_info['access_token']
            self.headers = {"Authorization": f"Bearer {access_token}"}
            print("Successfully authenticated.")
        else:
            print(f"Failed to authenticate: {response.content}")
    
    def list_dashboards(self) -> Optional[list]:
        dashboards_url = f"{self.base_url}/dashboard/"
        
        if not self.headers:
            print("Not authenticated.")
            return None
        
        response = requests.get(dashboards_url, headers=self.headers)
        
        if response.status_code == 200:
            dashboards = response.json()['result']
            return dashboards
        else:
            print(f"Failed to list dashboards: {response.content}")
            return None
    
    def get_dashboard_by_id(self, dashboard_id: int) -> Optional[dict]:
        dashboard_url = f"{self.base_url}/dashboard/{dashboard_id}"
        
        if not self.headers:
            print("Not authenticated.")
            return None
        
        response = requests.get(dashboard_url, headers=self.headers)
        
        if response.status_code == 200:
            dashboard = response.json()
            return dashboard
        else:
            print(f"Failed to get dashboard: {response.content}")
            return None
