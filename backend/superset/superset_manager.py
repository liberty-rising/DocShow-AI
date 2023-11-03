from typing import Optional

from utils.session_manager import SessionManager
from utils.utils import get_app_logger

import httpx

logger = get_app_logger(__name__)

class SupersetManager:
    def __init__(self, user_id: int, session_manager: SessionManager):
        self.base_url = "http://superset:8088/"
        self.api_url = f"{self.base_url}api/v1/"
        self.auth_url = f"{self.api_url}security/login"
        self.session = session_manager.get_session(user_id)
        self.authenticate_superset()
    
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
        csrf_url = f"{self.api_url}security/csrf_token/"
        self.session.headers['Referer'] = csrf_url
        csrf_res = self.session.get(csrf_url)
        csrf_res.raise_for_status()  # Check for HTTP errors
        self.session.headers['X-CSRFToken'] = csrf_res.json()['result']
    
    def get_or_create_database(self, db_manager):
        """
        Gets the ID of an existing database or creates a new database if it doesn't exist.

        Parameters:
            db_manager (ClientDatabaseManager): An instance of ClientDatabaseManager containing the database details.

        Returns:
            tuple: A tuple containing:
                - The ID (int or str) of the existing or newly-created database.
                - A boolean flag indicating whether a new database was created (True) or an existing one was found (False).
        """
        # Check if database exists
        database_id = self.get_database_id_by_name(db_manager.db_name)
        
        # If it does, return its ID
        if database_id:
            return database_id, False
        
        # If it doesn't, create it
        new_db_id = self.create_database_connection(
            db_name=db_manager.db_name,
            sqlalchemy_uri=db_manager.get_uri_str()
        )

        return new_db_id, True  # True indicates that a new database was created

    
    def get_database_id_by_name(self, db_name):
        self.get_csrf_token()
        db_list_url = f"{self.api_url}database/"
        response = self.session.get(db_list_url)
        if response.status_code == 200:
            databases = response.json()['result']
            for db in databases:
                if db['database_name'] == db_name:
                    return db['id']
        response.raise_for_status()  # This will raise an exception for non-2xx status codes, helping to debug any errors
        return None
    
    def create_database_connection(self, db_name, sqlalchemy_uri):
        self.get_csrf_token()
        db_payload = {
            "database_name": db_name,
            "engine": "postgresql",
            "configuration_method": "sqlalchemy_form",
            "sqlalchemy_uri": sqlalchemy_uri,
            # ... any other optional parameters
        }
        create_db_url = f"{self.api_url}database/"
        
        response = self.session.post(create_db_url, json=db_payload)

        if response.status_code == 201:
            print("Database connection created successfully")
            return response.json()["id"]
        else:
            print(f"Failed to create database connection: {response.text}")
            return None
    
    def get_or_create_dataset(self, dataset_payload):
        """
        Gets the ID of an existing dataset or creates a new one if it doesn't exist.

        Parameters:
            dataset_payload (dict): A dictionary containing the details of the dataset.
                                    Must include the key 'table_name'.

        Returns:
            tuple: A tuple containing:
                - The ID (int or str) of the existing or newly-created dataset.
                - A boolean flag indicating whether a new dataset was created (True) or an existing one was found (False).
        """
        # Check if database exists
        dataset_id = self.get_dataset_id_by_name(dataset_payload['table_name'])

        # If it does, return its ID
        if dataset_id:
            return dataset_id, False
        
        # If it doesn't, create it
        new_ds_id = self.create_dataset(dataset_payload)

        return new_ds_id, True
    
    def get_dataset_id_by_name(self, ds_name):
        self.get_csrf_token()
        dataset_url = f"{self.api_url}dataset/"
        response = self.session.get(dataset_url)

        if response.status_code == 200:
            datasets = response.json()['result']
            for ds in datasets:
                if ds['table_name'] == ds_name:
                    return ds['id']
        response.raise_for_status()
        return None

    
    def create_dataset(self, dataset_payload):
        self.get_csrf_token()
        dataset_url = f"{self.api_url}dataset/"
        response = self.session.post(dataset_url, json=dataset_payload)
        
        if response.status_code == 201:
            print("Successfully created dataset.")
            datasource_id = response.json().get("id", None)  # Replace 'id' with the actual key for the datasource ID in the response, if different
            return datasource_id
        else:
            print(f"Failed to create dataset: {response.content}")
    
    def get_or_create_chart(self, chart_payload):
        # Check if chart exists
        chart_id = self.get_chart_id_by_name(chart_payload['slice_name'])

        # If it does, return its ID
        if chart_id:
            return chart_id, False
        
        # If it doesn't, create it
        new_slice_id = self.create_chart(chart_payload)

        return new_slice_id, True
    
    def get_chart_id_by_name(self, slice_name):
        self.get_csrf_token()

        slice_url = f"{self.api_url}chart/"
        response = self.session.get(slice_url)

        if response.status_code == 200:
            slices = response.json()['result']
            for sl in slices:
                if sl['slice_name'] == slice_name:
                    return sl['id']
        response.raise_for_status()
        return None

    def create_chart(self, chart_payload):
        slice_url = f"{self.api_url}chart/"
        response = self.session.post(slice_url, json=chart_payload)
        if response.status_code == 201:
            print("Successfully created slice.")
            chart_data = response.json()
            return chart_data['id']
        else:
            print(f"Failed to create slice: {response.content}")
    
    def get_or_create_dashboard(self, dashboard_payload):
        """
        Fetches an existing dashboard by its title or creates a new one if it doesn't exist.
        
        Parameters:
            dashboard_payload (dict): The payload containing the details of the dashboard to be created.
                                    Must include the key 'dashboard_title'.
        
        Returns:
            tuple: A tuple containing the dashboard ID and a boolean flag.
                - The dashboard ID (int or str) is returned as the first element.
                - The boolean flag as the second element indicates whether a new dashboard was created (True) or not (False).
        """
        dashboard_id = self.get_dashboard_id_by_title(dashboard_payload['dashboard_title'])

        if dashboard_id is None:
            dashboard_id = self.create_dashboard(dashboard_payload)
            return dashboard_id, True
        return dashboard_id, False
    
    def get_dashboard_id_by_title(self, title):
        self.get_csrf_token()
        dashboard_url = f"{self.api_url}dashboard/"
        response = self.session.get(dashboard_url)
        if response.status_code == 200:
            dashboards = response.json()['result']
            for db in dashboards:
                if db['dashboard_title'] == title:
                    return db['id']
        return None

    def create_dashboard(self, dashboard_payload):
        self.get_csrf_token()
        dashboard_url = f"{self.api_url}dashboard/"
        response = self.session.post(dashboard_url, json=dashboard_payload)
        if response.status_code == 201:
            print("Successfully created dashboard.")
            return response.json()['id']
        else:
            print(f"Failed to create dashboard: {response.content}")
            return None
    
    def get_dashboard_by_id(self, dashboard_id: int):
        self.get_csrf_token()
        # TODO: I believe API authentication is not the same as user authentication and that's why it's not working
        response = self.session.get(f"{self.base_url}superset/dashboard/{dashboard_id}/?standalone=true")
        print(response)
        response.raise_for_status()
        return response
    
    def list_dashboards(self) -> Optional[list]:
        self.get_csrf_token()

        dashboards_url = f"{self.api_url}dashboard/"
        response = self.session.get(dashboards_url)
        if response.status_code == 200:
            dashboards = response.json()['result']
            return [(db['id'], db['dashboard_title']) for db in dashboards]
    
    def update_dashboard(self, dashboard_id, json_metadata):
        """
        Updates an existing dashboard with new JSON metadata.

        Parameters:
            dashboard_id (int or str): The ID of the dashboard to be updated.
            json_metadata_payload (dict): The payload containing the JSON metadata to update the dashboard with.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        self.get_csrf_token()
        url = f"{self.api_url}dashboard/{dashboard_id}"

        response = self.session.put(url, json=json_metadata)

        if response.status_code == 200:
            print("Successfully updated dashboard.")
            return True
        else:
            print(f"Failed to update dashboard: {response.content}")
            return False