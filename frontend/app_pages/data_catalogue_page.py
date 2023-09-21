import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from credentials import get_conn_str

def app():
    # Load the credentials from the credentials.py file
    conn_str = get_conn_str()

    # Create a SQLAlchemy engine with the connection string
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")

    # Get all table names with their schemas
    query_tables = """
    SELECT schema_name(schema_id) as schema_name, name as table_name
    FROM sys.tables;
    """
    tables_df = pd.read_sql(query_tables, engine)
    table_details = []

    for index, row in tables_df.iterrows():
        table_schema = row['schema_name']
        table_name = row['table_name']
        
        # Fetch number of rows
        query_rows = f"SELECT COUNT(*) FROM {table_schema}.{table_name}"
        num_rows = pd.read_sql(query_rows, engine).iloc[0, 0]

        # Fetch number of columns
        num_columns = len(pd.read_sql(f"SELECT TOP 1 * FROM {table_schema}.{table_name}", engine).columns)
        
        # Fetch creation datetime
        query_datetime = f"SELECT create_date FROM sys.tables WHERE schema_name(schema_id) = '{table_schema}' AND name = '{table_name}'"
        creation_datetime = pd.read_sql(query_datetime, engine).iloc[0, 0]
        
        table_details.append([f"{table_schema}.{table_name}", num_rows, num_columns, creation_datetime])

    df = pd.DataFrame(table_details, columns=["Table Name", "Number of Rows", "Number of Columns", "Creation Datetime"])

    st.write(df)

if __name__ == "__main__":
    app()
