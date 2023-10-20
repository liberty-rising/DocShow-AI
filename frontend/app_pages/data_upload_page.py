from io import StringIO
import streamlit as st
import pandas as pd
import PyPDF2
from sqlalchemy import create_engine, MetaData
from credentials import get_conn_str  # Ensure you have a credentials.py that contains this function

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def app():
    st.title("Data Upload")
    
    st.write("""
    ## Overview
    Welcome to the Data Upload page! This page provides an interface to upload and ingest your CSV or PDF files into the database.
    
    ### Features:
    - **File Type Selection**: Choose the type of file you want to upload (CSV or PDF).
    - **File Uploader**: Use the file uploader to select and upload your file.
    - **Preview**: Once uploaded, the top 5 rows of your data will be displayed for a quick preview.
    - **Custom Table Name**: Provide a custom name for the table when ingesting it into the database.
    - **Ingestion**: Click the 'Ingest into database' button to start the ingestion process. A progress bar and status updates will guide you through the process.
    
    To begin, select your file type and then upload your desired file.
    """)

    # Let the user choose the file type using radio buttons
    file_type = st.radio("Choose file type", ["CSV", "PDF"])

    # Create a file uploader widget
    uploaded_file = st.file_uploader(f"Upload {file_type} File")

    # Check if a file has been uploaded
    if uploaded_file is not None:
        if file_type == "CSV":
            df = pd.read_csv(uploaded_file)
        else:  # PDF
            text = extract_text_from_pdf(uploaded_file)
            delimiter = st.text_input("Specify the delimiter used in the PDF's tabular data (e.g., ',', '|', '\t' for tab):", ",")
            try:
                df = pd.read_csv(StringIO(text), delimiter=delimiter)
            except pd.errors.ParserError as e:
                st.error(f"Error parsing the PDF data: {e}")
                return
        
        st.write(df.head())

        # Let user provide custom table name
        user_table_name = st.text_input("Enter a custom table name (leave blank for default):")

        # Button to start the ingestion process
        if st.button("Ingest into database"):
            # Load the credentials from the credentials.py file
            conn_str = get_conn_str()

            # Create a SQLAlchemy engine with the connection string
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")

            # Create a metadata object to fetch table names
            metadata = MetaData()
            metadata.reflect(bind=engine)
            table_names = metadata.tables.keys()

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
            st.success(f"{file_type} file uploaded successfully!")
    else:
        st.info(f"Please upload a {file_type} file.")

if __name__ == "__main__":
    app()
