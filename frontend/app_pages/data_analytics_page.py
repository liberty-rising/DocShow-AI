import streamlit as st

from utils.utils import api_request, HEADERS

def app():
    st.title("📊 Data Analytics")

    st.write("""
    ## Overview
    Welcome to the Data Analytics page! This page provides an interface to gain insights from the data stored in the database.
    """)

    headers = HEADERS
    # Fetch list of available dashboards from FastAPI backend
    response = api_request("http://backend:8000/dashboards/", headers=headers)  # Replace with your FastAPI URL
    
    if response.status_code == 200:
        dashboards_data = response.json()["dashboards"]
        dashboard_options = {name: id_ for id_, name in dashboards_data}
    else:
        st.error("Failed to fetch available dashboards.")
        return

    # Allow user to select a dashboard
    selected_dashboard_name = st.selectbox("Choose a dashboard to view:", list(dashboard_options.keys()))

    # Get the selected dashboard ID
    selected_dashboard_id = dashboard_options[selected_dashboard_name]

    # # Embed the Superset dashboard
    # superset_url = f"http://superset:8088/superset/dashboard/{selected_dashboard_id}/?standalone=true"
    # st.components.v1.iframe(superset_url, width=800, height=600)
    # Fetch dashboard HTML from FastAPI backend
    response = api_request(f"http://backend:8000/dashboard/{selected_dashboard_id}", headers=headers)

    if response.status_code == 200:
        dashboard_html = response.text
        st.components.v1.html(dashboard_html, width=800, height=600)
    else:
        st.error("Failed to fetch dashboard.")

if __name__ == "__main__":
    app()
