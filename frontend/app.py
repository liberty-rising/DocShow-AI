# Your existing imports
import streamlit as st
from app_pages import (
    home_page,
    data_upload_page,
    ai_assistant_page,
    data_analytics_page,
    user_panel_page,
    admin_panel_page,
    login_page,
    registration_page
)
from utils import custom_css

# Add custom CSS for centered title
custom_css.add_css()

# If 'logged_in' not in session state, set it to False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# If not logged in, show login page
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.logged_in:
    SIDEBAR = {
        "🏠 Home": home_page,
        "📥 Data Upload": data_upload_page,
        "📊 Data Analytics": data_analytics_page,
        "💬 AI Assistant": ai_assistant_page,
        "👤 User Panel": user_panel_page,
        "⚙️ Admin Panel": admin_panel_page, 
    }

    with st.sidebar:
        st.markdown("<h1 style='text-align: left;'>👋 Welcome</h1>", unsafe_allow_html=True)
        
        # Create buttons for navigation
        for page_name in SIDEBAR.keys():
            if st.sidebar.button(page_name):
                st.session_state.page = page_name
        
    # st.session_state = "🏠 Home"
    SIDEBAR[st.session_state.page].app()

    # Sign out button logic
    with st.sidebar:
        if st.sidebar.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.experimental_rerun() 
else:
    if st.session_state.page == "login":
        login_page.app()
    elif st.session_state.page == "register":
        registration_page.app()