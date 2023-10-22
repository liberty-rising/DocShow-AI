# Your existing imports
import streamlit as st
from app_pages import home_page
from app_pages import data_upload_page
from app_pages import ai_assistant_page
from app_pages import data_catalogue_page
from app_pages import data_processing_page
from app_pages import data_analytics_page
from app_pages import machine_learning_page
from utils import custom_css

# Add custom CSS for centered title
custom_css.add_css()

# Reordered the pages for logical flow
PAGES = {
    "🏠 Home": home_page,
    "📥 Data Upload": data_upload_page,
    # "📖 Data Catalogue": data_catalogue_page,
    # "🔄 Data Processing": data_processing_page,
    "📊 Data Analytics": data_analytics_page,
    "🤖 AI Assisstant": ai_assistant_page,
    # "🖥️ Machine Learning": machine_learning_page,
    # "📈 Data Quality Dashboard": data_visualization_page,
}

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

with st.sidebar:
    st.markdown("<h1 style='text-align: left;'>👋 Welcome</h1>", unsafe_allow_html=True)
    
    # Create buttons for navigation
    for page_name in PAGES.keys():
        if st.sidebar.button(page_name):
            st.session_state.page = page_name

# Load the selected page
PAGES[st.session_state.page].app()
