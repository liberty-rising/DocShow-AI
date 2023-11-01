import httpx
import streamlit as st
import traceback
import pandas as pd

def check_file_constraints(file, file_type, encoding):
    if file_type not in ["csv", "xlsx"]:
        return "Invalid file type"
    
    if file_type == "csv" and encoding.lower() != "utf-8":
        return "Invalid encoding, should be UTF-8"

    try:
        if file_type == "csv":
            df = pd.read_csv(file, encoding=encoding)
        elif file_type == "xlsx":
            df = pd.read_excel(file)
    except Exception as e:
        return str(e)

    if df.columns.isnull().any():
        return "Missing header"

    if df.isna().mean().mean() > 0.2:
        return "More than 20 percent of rows have n/a values"

    return None

def app():
    st.title("📥 Data Upload")
    
    st.write("""
    ## Overview
    Welcome to the **Data Upload** page! Here, you can easily upload your data files into our system. This simple, user-friendly interface is designed to guide you through the process. 

    ### Steps:
    1. **Select File Type**: Choose the type of the file you're about to upload (e.g., CSV).
    2. **Choose Encoding**: For CSV files, select the appropriate file encoding.
    3. **Optional Description**: Add any extra description or comments about the file or data.
    4. **New Table**: Indicate whether the uploaded data should be stored in a new table.
    5. **Upload**: Finally, upload your file by clicking on 'Submit'.

    After uploading, you'll receive a confirmation message. If you encounter any issues, error messages will guide you on what went wrong.

    Happy uploading!
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
            encodings = client.get("http://backend:8000/encodings/", params={"file_type":file_type}).json()
            uppercased_encodings = [encoding.upper() for encoding in encodings]
        encoding = st.selectbox('Choose an encoding:', uppercased_encodings).lower()
    else:
        encoding = None

    # Add an extra message
    extra_desc = st.text_input("Add a description (optional)")

    # Figure out if a new table needs to be created
    is_new_table = st.radio("Is a new table needed?", ["Yes", "No"])

    # Create a file uploader widget
    with st.form(key='upload_form'):
        uploaded_file = st.file_uploader(f"Upload Your File")
        analyze_button = st.form_submit_button(label="Analyze")
        submit_button = st.form_submit_button(label="Submit")

    if analyze_button and uploaded_file is not None:
        # Perform checks
        check_result = check_file_constraints(uploaded_file, file_type, encoding)
        if check_result:
            st.error(f"File did not meet constraints: {check_result}")
        else:
            st.success("File meets all constraints")

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
                    timeout=60.0  # Timeout is in seconds
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
