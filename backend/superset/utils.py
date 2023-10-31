from databases.db_utils import ClientDatabaseManager
from superset.superset_manager import SupersetManager
from utils.utils import get_app_logger

import json

logger = get_app_logger(__name__)

def seed_superset():
    logger.debug("Starting seeding of Superset.")

    # Create an instance of SupersetManager
    superset_manager = SupersetManager()

    # Authenticate
    superset_manager.authenticate_superset()

    # Create database connection if it doesn't exist
    db_manager = ClientDatabaseManager()
    database_id, is_new_database = superset_manager.get_or_create_database(db_manager)
    logger.debug(f"Database id: {database_id} | New database: {is_new_database}")

    # Create a dataset if it doesn't exist
    dataset_payload = {
        "database": database_id,
        "schema": "public",
        "table_name": "sample_sales"
    }
    dataset_id, is_new_dataset = superset_manager.get_or_create_dataset(dataset_payload)
    logger.debug(f"Dataset id: {dataset_id} | New dataset: {is_new_dataset}")

    # Create a chart
    chart_payload = {
        "slice_name": "Sales by Status",
        "datasource_id":dataset_id,
        "datasource_type": "table",
        "viz_type":"pie",
        "params":json.dumps({
            "metric":{
                "aggregate":"SUM","column":{
                    "column_name":"sales"
                },
                "expressionType":"SIMPLE"
            },
            "groupby":["quantityordered"]
        })
    }
    chart_id, is_new_chart = superset_manager.get_or_create_chart(chart_payload)
    logger.debug(f"Chart id: {chart_id} | New chart: {is_new_chart}")

    # Create a dashboard
    dashboard_payload = {  
        "dashboard_title": "Sample Sales Dashboard",  # Name of the dashboard
        "published": True,  # Whether the dashboard is published
    }

    dashboard_id, is_new_dashboard = superset_manager.get_or_create_dashboard(dashboard_payload)
    logger.debug(f"Dashboard_id: {dashboard_id} | New dashboard: {is_new_dashboard}")

    if is_new_dashboard:
        # Prepare json_metadata payload
        json_metadata_payload = {  # Created by watching network feed in console while creating a dashboard in Superset UI
            "json_metadata": json.dumps({
                "positions":{
                    "DASHBOARD_VERSION_KEY":"v2","ROOT_ID":{"type":"ROOT","id":"ROOT_ID","children":["GRID_ID"]},
                    "GRID_ID":{"type":"GRID","id":"GRID_ID","children":["ROW-test"],"parents":["ROOT_ID"]},
                    "HEADER_ID":{"id":"HEADER_ID","type":"HEADER","meta":{"text":"Sample Sales Dashboard"}},
                    "CHART-test":{"type":"CHART","id":"CHART-test","children":[],"parents":["ROOT_ID","GRID_ID","ROW-test"],"meta":{"width":4,"height":50,"chartId":chart_id,"sliceName":"Sales by Status"}},
                    "ROW-test":{"type":"ROW","id":"ROW-test","children":["CHART-test"],"parents":["ROOT_ID","GRID_ID"],"meta":{"background":"BACKGROUND_TRANSPARENT"}}
                }
            })
        }
        # Update the dashboard
        superset_manager.update_dashboard(dashboard_id, json_metadata_payload)

    del superset_manager

    logger.debug("Seeding of Superset completed.")
