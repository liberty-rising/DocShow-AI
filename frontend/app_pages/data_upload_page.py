from io import StringIO
import httpx
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
    # file_type = st.radio("Choose file type", ["CSV", "PDF"])

    # Create a file uploader widget
    uploaded_file = st.file_uploader(f"Upload {file_type} File")

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Send a POST request with the file to the backend
        with httpx.Client() as client:
            response = client.post(
                "http://127.0.0.1:8000/upload",
                files={"file": uploaded_file}
            )

        # Check the response status code to see if the upload was successful
        if response.status_code == 200:
            st.success("File uploaded successfully!")
        else:
            st.error(f"Failed to upload file: {response.text}")
    else:
        st.info(f"Please upload a {file_type} file.")

if __name__ == "__main__":
    app()
