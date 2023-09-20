import streamlit as st
import pyodbc
import pandas as pd
from credentials import get_conn_str  # Ensure you have a credentials.py that contains this function

def app():
    # Load the credentials from the credentials.py file
    conn_str = get_conn_str()

    # Connect to the SQL Server database
    conn = pyodbc.connect(conn_str)

    # Initialize a cursor
    cur = conn.cursor()

    # Execute a query to find all existing tables in the database
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tables = cur.fetchall()

    # Create a Pandas DataFrame for better display
    df_tables = pd.DataFrame([table[0] for table in tables], columns=["Table Name"])

    # Display the tables in the Streamlit app
    st.header("Existing Tables")
    st.write(df_tables)

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload CSV File")

    # Check if a file has been uploaded
    if uploaded_file is not None:

        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Sanitize the column names in the DataFrame
        df.columns = df.columns.str.replace(" ", "_")

        # Create a new table name for the uploaded CSV file
        table_name = f"my_table_{len(tables) + 1}"

        # Check if the table name already exists in the database
        cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME = ?", (table_name,))
        if cur.fetchone() is not None:
            # If the table name already exists, generate a new table name
            table_name = f"my_table_{len(tables) + 2}"

        # Create a new table in the database
        column_types = "VARCHAR(MAX)"  # Here, I've set all columns to have the same data type for simplicity
        columns_with_types = [f"{col} {column_types}" for col in df.columns]
        cur.execute(f"CREATE TABLE {table_name} ({','.join(columns_with_types)})")

        # Insert the data from the DataFrame into the newly created table
        for index, row in df.iterrows():
            placeholders = ', '.join(['?'] * len(row))
            sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
            cur.execute(sql, tuple(row))

        # Commit the changes
        conn.commit()

        # Display a success message in the Streamlit app
        st.success("CSV file uploaded successfully!")

    else:
        st.info("Please upload a CSV file.")

if __name__ == "__main__":
    app()
