import streamlit as st
import httpx
from app_pages import registration_page

def app():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    login_button = st.button("Login")
    
    # Call backend API to authenticate
    if login_button:
        # Replace with actual authentication logic
        with httpx.Client() as client:
            response = client.post("http://backend:8000/token/", data={"username": username, "password": password})
        
        if response.status_code == 200:  # if login successful
            st.session_state.access_token = response.json()["access_token"]
            st.session_state.logged_in = True
            st.session_state.page = "🏠 Home"
            st.experimental_rerun() 
        else:
            st.error("Login failed. Check your credentials.")

    # Button to go to registration page
    if st.button("Register", key='reg_button'):
        st.session_state.page = "register"
        st.experimental_rerun()
