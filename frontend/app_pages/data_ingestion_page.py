import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData
from credentials import get_conn_str  # Ensure you have a credentials.py that contains this function

def app():
    # Load the credentials from the credentials.py file
    conn_str = get_conn_str()

    # Create a SQLAlchemy engine with the connection string
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")

    # Create a metadata object to fetch table names
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_names = metadata.tables.keys()

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload CSV File")

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame and display top 5 rows
        df = pd.read_csv(uploaded_file)
        st.write(df.head())

        # Let user provide custom table name
        user_table_name = st.text_input("Enter a custom table name (leave blank for default):")

        # Button to start the ingestion process
        if st.button("Ingest into database"):
            # Progress bar and status text initialization
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Sanitize column names
            status_text.text("Sanitizing column names...")
            df.columns = df.columns.str.replace(" ", "_")
            progress_bar.progress(25)

            # Generate table name
            status_text.text("Generating table name...")
            if user_table_name:  # if the user provided a table name
                table_name = user_table_name
            else:
                table_name = f"my_table_{len(table_names) + 1}"
                if table_name in table_names:
                    table_name = f"my_table_{len(table_names) + 2}"
            progress_bar.progress(50)

            # Insert DataFrame into the database
            status_text.text("Inserting data into the database...")
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            progress_bar.progress(100)

            # Finalize status updates
            status_text.text("Completed!")
            st.success("CSV file uploaded successfully!")
    else:
        st.info("Please upload a CSV file.")

if __name__ == "__main__":
    app()
