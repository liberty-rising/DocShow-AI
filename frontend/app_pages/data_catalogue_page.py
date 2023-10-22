import streamlit as st

def app():
    st.title("Data Catalogue")
    
    st.write("""
    ## Overview
    Welcome to the Data Catalogue page! This page provides an interface to view the list of tables stored in the database.
    
    ### Features:
    - **Upload and Display**: You can upload a CSV file, and it will be displayed on the page.
    - **Custom Table Name**: Provide a custom name for the table when ingesting it into the database.
    - **Refresh and Display**: By clicking the 'Refresh and display list of tables' button, the page fetches and displays the list of tables from the database.
    - **Progress Bar**: A progress bar indicates the progress of the table fetching process.
    
    Simply click the 'Refresh and display list of tables' button to view the current tables in the database.
    """)

    # if st.button("Refresh and display list of tables"):
    #     # Progress bar initialization
    #     progress = st.progress(0)
        
    #     # Load the credentials from the credentials.py file
    #     conn_str = get_conn_str()
    #     progress.progress(0.1)

    #     # Create a SQLAlchemy engine with the connection string
    #     engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
    #     progress.progress(0.2)

    #     # Get all table names with their schemas
    #     query_tables = """
    #     SELECT schema_name(schema_id) as schema_name, name as table_name
    #     FROM sys.tables;
    #     """
    #     tables_df = pd.read_sql(query_tables, engine)
    #     progress.progress(0.4)
    #     table_details = []

    #     for index, row in tables_df.iterrows():
    #         table_schema = row['schema_name']
    #         table_name = row['table_name']
            
    #         # Fetch number of rows
    #         query_rows = f"SELECT COUNT(*) FROM {table_schema}.{table_name}"
    #         num_rows = pd.read_sql(query_rows, engine).iloc[0, 0]

    #         # Fetch number of columns
    #         num_columns = len(pd.read_sql(f"SELECT TOP 1 * FROM {table_schema}.{table_name}", engine).columns)
            
    #         # Fetch creation datetime
    #         query_datetime = f"SELECT create_date FROM sys.tables WHERE schema_name(schema_id) = '{table_schema}' AND name = '{table_name}'"
    #         creation_datetime = pd.read_sql(query_datetime, engine).iloc[0, 0]
            
    #         table_details.append([f"{table_schema}.{table_name}", num_rows, num_columns, creation_datetime])
    #         progress.progress(0.6 + (0.2 * (index + 1) / len(tables_df)))

    #     df = pd.DataFrame(table_details, columns=["Table Name", "Number of Rows", "Number of Columns", "Creation Datetime"])
    #     st.write(df)
        
    #     progress.progress(1.0)
    #     st.success("List of tables has been refreshed.")
    # else:
    #     st.info("Click the button to fetch and display the list of tables.")

if __name__ == "__main__":
    app()
