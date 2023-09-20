# Your existing imports
import streamlit as st
import home_page 
import data_catalogue_page 
import data_processing_page 
import data_analytics_page
import data_visualization_page

# import machine_learning_page
# import llm_page  # Import the new LLM page
from utils import custom_css

# Add custom CSS for centered title
custom_css.add_css()

# Path to the local image
image_path = './utils/logo.jpg'  # Replace 'your_logo.jpg' with the actual file name


# Reordered the pages for logical flow and added LLM page
PAGES = {
    "🏠 Home": home_page,
    "📖 Data Catalogue": data_catalogue_page,
    "🔄 Data Processing": data_processing_page,
    "📊 Data Analytics": data_analytics_page,
    "📈 Data Visualization": data_visualization_page,
    # "🤖 Machine Learning": machine_learning_page,
    # "🦙 LLM": llm_page  # New LLM page with llama emoji
}

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

with st.sidebar:
    st.image(image_path, caption='', use_column_width=True)  # Display the image
    st.markdown("<h1 style='text-align: left;'>👋 Welcome</h1>", unsafe_allow_html=True)

    # Create buttons for navigation, reordered for logical flow
    if st.sidebar.button("🏠 Home"):
        st.session_state.page = "🏠 Home"
    if st.sidebar.button("📖 Data Catalogue"):
        st.session_state.page = "📖 Data Catalogue"
    if st.sidebar.button("🔄 Data Processing"):
        st.session_state.page = "🔄 Data Processing"
    if st.sidebar.button("📊 Data Analytics"):
        st.session_state.page = "📊 Data Analytics"
    if st.sidebar.button("📈 Data Visualization"):
        st.session_state.page = "📈 Data Visualization"
    if st.sidebar.button("🤖 Machine Learning"):
        st.session_state.page = "🤖 Machine Learning"
    if st.sidebar.button("🦙 LLM"):  # New LLM button with llama emoji
        st.session_state.page = "🦙 LLM"

# Load the selected page
PAGES[st.session_state.page].app()


