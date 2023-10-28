from databases.db_utils import ClientDatabaseManager
from superset.superset_manager import SupersetManager

import json

def seed_superset():
    # Create an instance of SupersetManager
    superset_manager = SupersetManager()

    # Authenticate
    superset_manager.authenticate_superset()

    # Create database connection if it doesn't exist
    db_manager = ClientDatabaseManager()
    if not superset_manager.database_exists(db_manager.db_name):
        superset_manager.create_database_connection(
            db_name=db_manager.db_name,
            sqlalchemy_uri=db_manager.get_uri_str()
        )

    # Now, get the database ID
    database_id = superset_manager.get_database_id("client_db")

    # Create a datasource if it doesn't exist
    datasource_payload = {
        "database": database_id,
        "schema": "public",
        "table_name": "sample_sales"
    }
    datasource_id = superset_manager.get_or_create_datasource(datasource_payload)

    # Create a slice (chart)
    slice_payload = {
        "slice_name": "Sales by Status",
        "viz_type": "pie",
        "datasource_id": datasource_id,
        "datasource_type": "table",
        "params": json.dumps({
            "metric": [{"expressionType": "SIMPLE", "column": {"column_name": "sales", "type": "DOUBLE"}, "aggregate": "SUM"}],
            "groupby": ["status"],
            "adhoc_filters": []
        })
    }
    slice_id = superset_manager.get_or_create_slice(slice_payload)

    # Create a dashboard
    dashboard_payload = {
        "dashboard_title": "Sample Sales Dashboard",  # Name of the dashboard
        "published": True,  # Whether the dashboard is published
        "position_json": json.dumps({
            "DASHBOARD_VERSION_KEY": "v2",
            "ROOT_ID": "ROOT_ID",
            "ROOT_TYPE": "ROOT",
            "GRID_ID": "GRID_ID",
            "GRID_TYPE": "GRID",
            "HEADER_ID": "HEADER_ID",
            "HEADER_TYPE": "HEADER",
            "TABS_ID": "TABS_ID",
            "TABS_TYPE": "TABS",
            "TAB_ID": "TAB_ID",
            "TAB_TYPE": "TAB",
            "CHART_ID": slice_id,  # Replace with your actual slice ID
            "CHART_TYPE": "CHART",
            "ROW_ID": "ROW_ID",
            "ROW_TYPE": "ROW",
        })}
    superset_manager.get_or_create_dashboard(dashboard_payload)

    del superset_manager
