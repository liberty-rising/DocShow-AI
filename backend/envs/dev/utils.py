from databases.database_managers import ClientDatabaseManager
from databases.sql_executor import SQLExecutor
from databases.table_manager import TableManager

import pandas as pd

def seed_client_db():
    """
    Asynchronously seed the client database with sample data from CSV files.
    
    The function only creates tables that don't already exist in the database.
    
    Internal Variables:
    - sample_tables: Dictionary mapping table names to corresponding CSV file names.
    - existing_tables: List of table names that already exist in the database.
    - session: Database session managed by ClientDatabaseManager.
    - executor: Instance of SQLExecutor for executing SQL queries.
    - manager: Instance of TableManager for table operations.
    
    Workflow:
    1. Initialize `sample_tables` dictionary to hold table-to-file mappings.
    2. Use ClientDatabaseManager to create a session and SQLExecutor to get existing table names.
    3. Loop through `sample_tables` and create tables if they don't exist, using data from CSV files.
    """
    sample_tables = {
        "sample_sales":"sample_sales_data.csv"
    }

    with ClientDatabaseManager() as session:
        executor = SQLExecutor(session)
        existing_tables = executor.get_all_table_names_as_list()

    manager = TableManager()
    
    for table_name, data_file in sample_tables.items():
        if table_name not in existing_tables:
            df = pd.read_csv(f"envs/dev/sample_data/{data_file}")
            df.columns = map(str.lower, df.columns)
            manager.create_table_from_df(df, table_name)

