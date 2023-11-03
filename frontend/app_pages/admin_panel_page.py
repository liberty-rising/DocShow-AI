import httpx
import streamlit as st

from utils.utils import api_request

import pandas as pd


def app():
    st.title("⚙️ Admin Panel")

    st.subheader("Table management")
    tables = api_request("http://backend:8000/tables/").json()

    selected_table = st.selectbox('Choose a table to drop:', tables)
    
    if st.button("Drop Table"):
        params={"table_name":selected_table}
        response = api_request("http://backend:8000/table/", "DELETE", params=params)
        
        if response.status_code == 200:
            st.write(f"Successfully dropped table {selected_table}.")
        else:
            st.write(f"Failed to drop table {selected_table}.")
    
    if st.button("Refresh"):
        st.experimental_rerun()
    
    st.subheader("User management")
    users_data = api_request("http://backend:8000/users/").json()
    roles_data = api_request("http://backend:8000/users/roles/").json()

    df = pd.DataFrame(users_data)

    st.table(df)

    # Display users in a SelectBox
    user_names = [user['username'] for user in users_data]
    selected_user_name = st.selectbox('Choose a user to edit:', user_names)
    selected_user = next((user for user in users_data if user['username'] == selected_user_name), None)

    # Editable fields for Organization and Role
    new_org = st.text_input("Organization", selected_user['organization'])
    selected_role = st.selectbox("Select a new role:", roles_data)
    
    if st.button("Update"):
        # Send the updated organization and role to the backend
        data = {
            'username': selected_user_name,
            'organization': new_org,
            'role': selected_role
        }
        response = api_request("http://backend:8000/users/update/", "PUT", json=data)
        
        if response.status_code == 200:
            st.write(f"Successfully updated details for {selected_user_name}.")
            st.experimental_rerun() 
        else:
            st.write(f"Failed to update details for {selected_user_name}.")

if __name__ == "__main__":
    app()