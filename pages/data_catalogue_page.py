import base64  # For file download
import streamlit as st
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
import os
import pyodbc  # For Azure SQL database
from credentials import get_conn_str
# from custom_functions import map_dtype

def map_dtype(dtype):
    if "int" in dtype:
        return "INT"
    elif "float" in dtype:
        return "FLOAT"
    elif "object" in dtype:
        return "VARCHAR(255)"
    else:
        return "VARCHAR(255)"  # Default data type


def app():
    df = None  # Initialize df to None

    # Check if a dataset already exists
    if os.path.exists('./dataset.csv'):
        df = pd.read_csv('dataset.csv', index_col=None)

    choice = st.radio("Navigation", ["Check database tables list","Upload file to database"])

    if choice == "Upload file to database":
        st.title("Upload Your Dataset")
        file = st.file_uploader("Upload Your Dataset", type=["csv"])
        
        # Read and display the uploaded CSV file
        if file:
            df = pd.read_csv(file, index_col=None)
            df.to_csv('dataset.csv', index=None)
            st.dataframe(df)  # Display the dataframe as a table

            # Replace NaN values with a default value
            df.fillna(0, inplace=True)  # Replace NaN with 0

            # Explicitly convert to float
            for col in df.select_dtypes(include=['float64']).columns:
                df[col] = df[col].astype(float)

            # Button to ingest data into Azure SQL database
            if st.button("Ingest into Database"):
                # Azure SQL database connection string
                conn_str = get_conn_str()
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()

                # Check if table exists
                cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'my_table'")
                if not cursor.fetchone():
                    # Create table with the same column names as in the DataFrame
                    columns = ", ".join([f"{col} {map_dtype(str(df.dtypes[col]))}" for col in df.columns])
                    create_table_query = f"CREATE TABLE my_table ({columns})"
                    cursor.execute(create_table_query)
                    conn.commit()

                # Ingest data into the table
                for index, row in df.iterrows():
                    try:
                        placeholders = ', '.join('?' * len(row))
                        insert_query = f"INSERT INTO my_table VALUES ({placeholders})"
                        cursor.execute(insert_query, tuple(row))
                    except Exception as e:
                        st.error(f"Error inserting row {index}: {e}")

                conn.commit()
                conn.close()
                st.success("Data ingested into Azure SQL database successfully!")

    if choice == "Check database tables list":
        st.title("Database Tables")
        
        # Azure SQL database connection string
        conn_str = get_conn_str()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Execute SQL query to get table names
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        
        # Fetch all table names
        tables = [table[0] for table in cursor.fetchall()]
        
        # Search box for tables
        search_query = st.text_input("Search for tables")
        
        # Filter table list based on search query
        filtered_tables = [table for table in tables if search_query.lower() in table.lower()]
        
        # Dropdown to select a table, default is None
        selected_table = st.selectbox("Select a table", [None] + filtered_tables)
        
        # Fetch and display top 3 rows from the selected table
        if selected_table:
            cursor.execute(f"SELECT TOP 3 * FROM {selected_table}")  # Changed to TOP 3
            top_3_rows = cursor.fetchall()  # Renamed to top_3_rows
            column_names = [column[0] for column in cursor.description]
            
            # Create a DataFrame to display in Streamlit
            df_top_3 = pd.DataFrame.from_records(top_3_rows, columns=column_names)  # Renamed to df_top_3
            st.table(df_top_3)
        
        # Initialize list to hold table details
        table_details = []
        
        # Only proceed if a table is selected
        if selected_table:
            for table_name in tables:
                
                # Get number of columns
                cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
                num_columns = cursor.fetchone()[0]
                
                # Get number of rows
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                num_rows = cursor.fetchone()[0]
                
                # Get creation date (Note: SQL Server specific query)
                cursor.execute(f"SELECT create_date FROM sys.tables WHERE name = '{table_name}'")
                created_at = cursor.fetchone()[0]
                
                # Append details to list
                table_details.append([table_name, num_columns, num_rows, created_at])
            
            # Create a DataFrame to display in Streamlit
            df_tables = pd.DataFrame(table_details, columns=['Table Name', 'Number of Columns', 'Number of Rows', 'Created At'])
            st.table(df_tables)
        
        # Close the connection
        conn.close()

    
