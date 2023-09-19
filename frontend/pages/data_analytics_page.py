import streamlit as st
import pandas as pd
import pyodbc  # For Azure SQL database
from frontend.credentials import get_conn_str  # Assuming you have a credentials.py file

def app():
    st.title("Data Analytics")

    # Initialize DataFrame
    df = None

    # Radio button to select data source
    data_source = st.radio("Choose your data source:", ["Upload CSV File", "Select Database Table"])

    if data_source == "Upload CSV File":
        uploaded_file = st.file_uploader("Upload your CSV file:", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Uploaded data:")
            st.dataframe(df)

    elif data_source == "Select Database Table":
        # Azure SQL database connection string
        conn_str = get_conn_str()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Execute SQL query to get table names
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tables = [table[0] for table in cursor.fetchall()]

        # Dropdown to select a table
        selected_table = st.selectbox("Select a table", [None] + tables)

        # Fetch and display top 3 rows from the selected table
        if selected_table:
            cursor.execute(f"SELECT TOP 3 * FROM {selected_table}")
            top_3_rows = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            
            # Create a DataFrame to display in Streamlit
            df = pd.DataFrame.from_records(top_3_rows, columns=column_names)
            st.write("Selected table data:")
            st.dataframe(df)

        # Close the connection
        conn.close()

    # Generate report if DataFrame is not empty
    if df is not None:
        st.write("### Data Overview")
        
        # Use Streamlit's native features for data exploration
        st.write("#### Data Summary")
        st.write(df.describe())
        
        st.write("#### Data Types")
        st.write(df.dtypes)
        
        st.write("#### Missing Values")
        st.write(df.isnull().sum())

        # Add more data exploration features as needed
