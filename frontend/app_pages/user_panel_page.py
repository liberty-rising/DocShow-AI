import httpx
import streamlit as st

def app():
    st.title("👤 User Panel")

    # Get current user data
    url = "http://backend:8000/users/me/"

    # Set up the headers with the token
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}"
    }

    with httpx.Client() as client:
        response = client.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        user_data = response.json()

        st.write(f"Your organisation: {user_data['organization']}")
        st.write(f"Your role: {user_data['role']}")
    else:
        st.error("Failed to fetch user details.")

if __name__ == "__main__":
    app()