import httpx
import streamlit as st
import traceback


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
    with httpx.Client() as client:
        file_types = client.get(
            "http://backend:8000/file_types/",
        ).json()
        uppercased_file_types = [file_type.upper() for file_type in file_types]
    file_type = st.radio("Choose file type", uppercased_file_types).lower()
    
    if file_type == "csv":
        with httpx.Client() as client:
            encodings = client.get(
                "http://backend:8000/encodings/",
                params={"file_type":file_type}
            ).json()
            uppercased_encodings = [encoding.upper() for encoding in encodings]

        encoding = st.selectbox('Choose an encoding:', uppercased_encodings).lower()

    # Add an extra message
    extra_desc = st.text_input("Add a description (optional)")

    # Figure out if a new table needs to be created
    is_new_table = st.radio("Is a new table needed?", ["Yes", "No"])

    # Create a file uploader widget
    with st.form(key='upload_form'):
        uploaded_file = st.file_uploader(f"Upload Your File")
        submit_button = st.form_submit_button(label="Submit")

    # Check if a file has been uploaded
    if submit_button and uploaded_file is not None:
        data = {
        'extra_desc': extra_desc if extra_desc else "",
        'is_new_table': is_new_table == "Yes",
        'encoding': encoding if encoding else "",
        }

        try:
            # Send a POST request with the file to the backend
            with httpx.Client() as client:
                response = client.post(
                    "http://backend:8000/upload/",
                    files={"file": uploaded_file},
                    data=data,
                    timeout=30.0  # Timeout is in seconds
                )
            
            # Check the response status code to see if the upload was successful
            if response.status_code == 200:
                st.success("File uploaded successfully!")
            else:
                st.error(f"Failed to upload file: {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.text(traceback.format_exc())

    else:
        st.info(f"Please upload a file.")

if __name__ == "__main__":
    app()
