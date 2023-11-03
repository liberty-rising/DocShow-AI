# registration_page.py
import streamlit as st
from utils.utils import api_request

def app():
    st.title("User Registration")

    username = st.text_input("Username", key="reg_username")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")

    submit = st.button("Register")

    if submit:
        # API endpoint
        url = "http://backend:8000/register/"
        
        # Form payload
        payload = {
            "username": username,
            "email": email,
            "password": password,
        }

        response = api_request(url, "POST", json=payload)

        # Handle response
        if response.status_code == 200:
            st.success("Successfully registered!")
            st.session_state.page = "login"
            st.experimental_rerun()
        else:
            st.error(f"Error occurred: {response.text}")
    
    if st.button("Back to login"):
        st.session_state.page = "login"
        st.experimental_rerun()
