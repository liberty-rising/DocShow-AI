import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.title("Data Analytics")

    st.write("""
    ## Overview
    Welcome to the Data Analytics page! This page provides an interface to gain insights from the data stored in the database.
    """)

    # Embed Superset dashboard
    superset_url = "http://superset:8088"
    st.components.v1.iframe(superset_url, width=800, height=600)

if __name__ == "__main__":
    app()
