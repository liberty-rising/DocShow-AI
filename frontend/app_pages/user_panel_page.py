import httpx
import streamlit as st

from utils.utils import api_request, HEADERS

def app():
    st.title("👤 User Panel")

    headers = HEADERS

    # Get current user data
    url = "http://backend:8000/users/me/"

    response = api_request(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        user_data = response.json()

        st.write(f"Your organisation: {user_data['organization']}")
        st.write(f"Your role: {user_data['role']}")
    else:
        st.error("Failed to fetch user details.")

if __name__ == "__main__":
    app()