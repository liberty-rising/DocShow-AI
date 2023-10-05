import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, OneHotEncoder
from credentials import get_conn_str
import base64

def load_tables_from_db(conn_str):
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return list(metadata.tables.keys())

def load_data_from_table(table_name, conn_str):
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

def generate_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Report</a>'
    return href

def app():
    st.title("Machine Learning Data Preparation")

    # Initialize or get the state
    if 'connected' not in st.session_state:
        st.session_state.connected = False
    if 'selected_table' not in st.session_state:
        st.session_state.selected_table = None
    if 'df' not in st.session_state:
        st.session_state.df = None

    if st.button("1. Connect to Database") or st.session_state.connected:
        st.session_state.connected = True
        # Load table names from the database
        tables = load_tables_from_db(get_conn_str())
        st.session_state.selected_table = st.selectbox("Choose a table from the database:", ["Select a table..."] + tables)

        # If a table is selected, load its data
        if st.session_state.selected_table != "Select a table..." and st.session_state.df is None:
            st.session_state.df = load_data_from_table(st.session_state.selected_table, get_conn_str())
            st.success(f"Loaded {st.session_state.df.shape[0]} rows and {st.session_state.df.shape[1]} columns from {st.session_state.selected_table}")

        # EDA: Display summary statistics
        if st.button("2. Show Summary Statistics"):
            st.write(st.session_state.df.describe())

        # Convert categorical variables to numerical form using OneHotEncoder
        if st.button("3. Convert Categorical Variables using OneHotEncoder"):
            st.session_state.df = pd.get_dummies(st.session_state.df, drop_first=True)
            st.success("Categorical variables converted to numerical form using OneHotEncoder.")
            st.markdown(generate_download_link(st.session_state.df, "encoded_data_report.csv"), unsafe_allow_html=True)

        # Correlation Analysis
        if st.button("4. Remove Highly Correlated Features"):
            non_numeric_cols = st.session_state.df.select_dtypes(include=['object']).columns.tolist()
            if not non_numeric_cols:
                correlation_matrix = st.session_state.df.corr().abs()
                upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(np.bool))
                to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > 0.95)]
                st.session_state.df.drop(to_drop, axis=1, inplace=True)
                st.success(f"Removed correlated features. Remaining columns: {st.session_state.df.shape[1]}")
            else:
                st.error(f"Please ensure all categorical variables are encoded before removing correlated features. Non-numeric columns: {', '.join(non_numeric_cols)}")

        # Data Splitting
        train_size = st.slider("5. Choose Training Set Size:", 0.1, 0.9, 0.7)
        if st.button("6. Split Data into Training and Testing Sets"):
            train_df = st.session_state.df.sample(frac=train_size, random_state=42)
            test_df = st.session_state.df.drop(train_df.index)
            st.success(f"Training set: {train_df.shape[0]} rows, Testing set: {test_df.shape[0]} rows")

        # Data Transformation: Min-Max Scaling
        if st.button("7. Apply Min-Max Scaling"):
            scaler = MinMaxScaler()
            st.session_state.df = pd.DataFrame(scaler.fit_transform(st.session_state.df), columns=st.session_state.df.columns)
            st.success("Min-Max scaling applied.")
            st.markdown(generate_download_link(st.session_state.df, "scaled_data_report.csv"), unsafe_allow_html=True)

if __name__ == "__main__":
    app()
