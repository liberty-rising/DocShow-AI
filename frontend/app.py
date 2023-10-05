# Your existing imports
import streamlit as st
from app_pages import home_page
from app_pages import data_ingestion_page
from app_pages import data_catalogue_page
from app_pages import data_processing_page
from app_pages import data_analytics_page
from app_pages import machine_learning_page
#data_processing_page, data_analytics_page, data_quality_dashboard_page, 
from utils import custom_css

# Add custom CSS for centered title
custom_css.add_css()

# Reordered the pages for logical flow
PAGES = {
    "🏠 Home": home_page,
    "📥 Data Ingestion": data_ingestion_page,
    "📖 Data Catalogue": data_catalogue_page,
    "🔄 Data Processing": data_processing_page,
    "📊 Data Analytics": data_analytics_page,
    "🤖 Machine Learning": machine_learning_page,
    # Uncomment these if you have these pages ready
    # "📈 Data Quality Dashboard": data_visualization_page,

    # "🦙 LLM": llm_page  # New LLM page with llama emoji
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
