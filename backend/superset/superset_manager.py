import httpx
from typing import Optional

class SupersetManager:
    def __init__(self):
        self.base_url = "http://superset:8088/api/v1"
        self.auth_url = f"{self.base_url}/security/login"
        self.session = httpx.Client()  # Create a session object for making requests
    
    def authenticate_superset(self):
        payload = {
            "username": "admin",
            "password": "adminpassword",
            "provider": "db"
        }
        response = self.session.post(self.auth_url, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        auth_data = response.json()
        self.session.headers['Authorization'] = f"Bearer {auth_data['access_token']}"
        self.session.headers['Content-Type'] = 'application/json'
    
    def get_csrf_token(self):
        csrf_url = f"{self.base_url}/security/csrf_token/"
        self.session.headers['Referer'] = csrf_url
        csrf_res = self.session.get(csrf_url)
        csrf_res.raise_for_status()  # Check for HTTP errors
        self.session.headers['X-CSRFToken'] = csrf_res.json()['result']
    
    def database_exists(self, db_name):
        db_list_url = f"{self.base_url}/database/"
        response = self.session.get(db_list_url)
        if response.status_code == 200:
            databases = response.json()['result']
            return any(db['database_name'] == db_name for db in databases)
        response.raise_for_status()  # This will raise an exception for non-2xx status codes, helping to debug any errors
        return False
    
    def create_database_connection(self, db_name, sqlalchemy_uri):
        self.get_csrf_token()
        db_payload = {
            "database_name": db_name,
            "engine": "postgresql",
            "configuration_method": "sqlalchemy_form",
            "sqlalchemy_uri": sqlalchemy_uri,
            # ... any other optional parameters
        }
        create_db_url = f"{self.base_url}/database/"
        
        response = self.session.post(create_db_url, json=db_payload)

        if response.status_code == 201:
            print("Database connection created successfully")
        else:
            print(f"Failed to create database connection: {response.text}")
    
    def list_dashboards(self) -> Optional[list]:
        self.get_csrf_token()
        dashboards_url = f"{self.base_url}/dashboard/"
        
        if not self.session.headers.get('Authorization'):
            print("Not authenticated.")
            return None
        
        response = self.session.get(dashboards_url)
        
        if response.status_code == 200:
            dashboards = response.json()['result']
            return [(db['id'], db['dashboard_title']) for db in dashboards]
        else:
            print(f"Failed to list dashboards: {response.content}")
            return None
    
    def get_dashboard_by_id(self, dashboard_id: int) -> Optional[dict]:
        dashboard_url = f"{self.base_url}/dashboard/{dashboard_id}"
        
        if not self.session.headers.get('Authorization'):
            print("Not authenticated.")
            return None
        
        response = self.session.get(dashboard_url)
        
        if response.status_code == 200:
            dashboard = response.json()
            return dashboard
        else:
            print(f"Failed to get dashboard: {response.content}")
            return None
    
    def get_or_create_datasource(self, datasource_payload):
        self.get_csrf_token()
        datasource_url = f"{self.base_url}/dataset/"
        response = self.session.get(datasource_url)
        
        if response.status_code == 200:
            datasources = response.json()['result']
            for ds in datasources:
                if ds['table_name'] == datasource_payload['table_name']:
                    return ds['id']
            self.create_datasource(datasource_payload)
            return None  # Fetch the newly created datasource ID or return None if needed
        else:
            print(f"Failed to fetch datasources: {response.text}")
            return None
    
    def create_datasource(self, datasource_payload):
        datasource_url = f"{self.base_url}/dataset/"
        response = self.session.post(datasource_url, json=datasource_payload)
        
        if response.status_code == 201:
            print("Successfully created datasource.")
            print('DATAAAAA',datasource_id)
            datasource_id = response.json().get("id", None)  # Replace 'id' with the actual key for the datasource ID in the response, if different
            return datasource_id
        else:
            print(f"Failed to create datasource: {response.content}")
    
    def get_or_create_slice(self, slice_payload):
        self.get_csrf_token()
        slice_url = f"{self.base_url}/chart/"
        response = self.session.get(slice_url)
        if response.status_code == 200:
            slices = response.json()['result']
            for sl in slices:
                if sl['slice_name'] == slice_payload['slice_name']:
                    return sl['id']
            self.create_slice(slice_payload)
            return None  # Fetch the newly created slice ID or return None if needed
        else:
            print(f"Failed to fetch slices: {response.text}")
            return None

    def create_slice(self, slice_payload):
        slice_url = f"{self.base_url}/chart/"
        response = self.session.post(slice_url, json=slice_payload)
        if response.status_code == 201:
            print("Successfully created slice.")
            slice_data = response.json()
            return slice_data['id']
        else:
            print(f"Failed to create slice: {response.content}")
    
    def get_or_create_dashboard(self, dashboard_payload):
        self.get_csrf_token()
        dashboard_url = f"{self.base_url}/dashboard/"
        response = self.session.get(dashboard_url)
        if response.status_code == 200:
            dashboards = response.json()['result']
            for db in dashboards:
                if db['dashboard_title'] == dashboard_payload['dashboard_title']:
                    return db['id']
            self.create_dashboard(dashboard_payload)
            return None  # Fetch the newly created dashboard ID or return None if needed
        else:
            print(f"Failed to fetch dashboards: {response.text}")
            return None

    def create_dashboard(self, dashboard_payload):
        dashboard_url = f"{self.base_url}/dashboard/"
        response = self.session.post(dashboard_url, json=dashboard_payload)
        if response.status_code == 201:
            print("Successfully created dashboard.")
        else:
            print(f"Failed to create dashboard: {response.content}")
    
    def get_database_id(self, db_name: str) -> Optional[int]:
        db_list_url = f"{self.base_url}/database/"
        response = self.session.get(db_list_url)
        if response.status_code == 200:
            databases = response.json()['result']
            for db in databases:
                if db['database_name'] == db_name:
                    return db['id']
        else:
            response.raise_for_status()  # raise HTTP error if any
        return None
    
    def __del__(self):
        self.session.close()