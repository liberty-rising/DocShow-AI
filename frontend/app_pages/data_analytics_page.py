import streamlit as st

from utils.utils import api_request, get_headers

def app():
    st.title("📊 Data Analytics")

    st.write("""
    ## Overview
    Welcome to the Data Analytics page! This page provides an interface to gain insights from the data stored in the database.
    """)

    headers = get_headers()
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

    # Fetch dashboard HTML from FastAPI backend
    # dashboard_data = api_request(f"http://backend:8000/dashboard/{selected_dashboard_id}", headers=headers).json()
    iframe_html = f"""
    <iframe
        title="Dashboard"
        src="http://127.0.0.1:8088/login?token=1967b4d50a5fb9a9e2c78f3bf8e8794f05737536d518b14a63ec20fe5ab6a672&next=/superset/dashboard/1?standalone=3"
        width="100%"
        height="800"
        sandbox="allow-same-origin allow-scripts"
    ></iframe>
    """
    # if dashboard_data:
    #     # st.components.v1.html(iframe_html, width=800, height=800)
    # else:
    #     st.error("Failed to fetch dashboard.")

    st.components.v1.html(f'<iframe src="http://backend:8000/dashboard/{selected_dashboard_id}" width="100%" height="800" sandbox="allow-same-origin allow-scripts></iframe>', height=800)


if __name__ == "__main__":
    app()
