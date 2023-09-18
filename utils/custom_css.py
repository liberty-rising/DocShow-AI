import streamlit as st

def add_css():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )