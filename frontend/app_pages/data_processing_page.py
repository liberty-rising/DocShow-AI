import streamlit as st
import pandas as pd
import numpy as np

def app():
    st.title("Data Processing")
    
    st.write("""
    ## Overview
    Welcome to the Data Processing page! This page provides an interface to process and clean your data stored in the database.
    
    ### Features:
    - **Table Selection**: Choose a table from the dropdown to process its data.
    - **Data Quality Statistics**: Click the 'Show Data Quality Statistics' button to view various statistics about the data quality of the selected table.
    - **Data Cleaning Options**: Use the radio buttons to select a data cleaning operation. Options include dropping NA values, replacing zeros, filling NA values, dropping duplicates, and removing outliers.
    - **Save Cleaned Data**: After performing a cleaning operation, click the 'Save Cleaned Data' button to save the cleaned data back to the database.
    
    To begin, connect to the database and select a table from the dropdown to explore the available features.
    """)

    # Check if 'connected' is already in the session state
    if 'connected' not in st.session_state:
        st.session_state.connected = False

    if st.button("Connect to database"):
        st.session_state.connected = True

    if st.session_state.connected:
        table_name = st.selectbox("Choose a table", ["Select a table..."] + get_table_names())
        
        if table_name != "Select a table...":
            df = get_table_data(table_name)

            if st.button("Show Data Quality Statistics"):
                show_data_quality(df)

            st.write("### Data Cleaning Options")
            selected_operation = st.radio("Choose a cleaning operation", ["Drop NA values", "Replace zeros", "Fill NA values", "Drop duplicates", "Remove outliers"])
            cleaned_df = clean_data(df, selected_operation)

            if st.button("Save Cleaned Data"):
                progress = st.progress(0)
                status = st.empty()
                save_cleaned_data(table_name, cleaned_df, progress, status)

# def get_table_names():
#     conn_str = get_conn_str()
#     with pyodbc.connect(conn_str) as conn:
#         query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"
#         tables = pd.read_sql(query, conn)
#     return tables['TABLE_NAME'].tolist()

# def get_table_data(table_name):
#     conn_str = get_conn_str()
#     with pyodbc.connect(conn_str) as conn:
#         df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
#     return df

# def save_cleaned_data(table_name, df, progress, status):
#     conn_str = get_conn_str()
#     with pyodbc.connect(conn_str) as conn:
#         cursor = conn.cursor()
#         cursor.execute(f"DELETE FROM {table_name}")
#         tuples = [tuple(x) for x in df.to_numpy()]
#         cols = ','.join(list(df.columns))
#         query = f"INSERT INTO {table_name} ({cols}) VALUES ({','.join(['?'] * len(df.columns))})"
#         cursor.executemany(query, tuples)
#         conn.commit()
#         progress.progress(100)
#         status.text("Data saved successfully!")

# def show_data_quality(df):
#     st.write("### Missing Values")
#     st.write(f"Total Rows: {len(df)}")
#     st.write(df.isnull().sum())
#     st.write("### Duplicates")
#     st.write(df.duplicated().sum())
#     st.write("### Data Types")
#     st.write(df.dtypes)
#     st.write("### Unique Values")
#     st.write(df.nunique())
#     st.write("### Zeros")
#     st.write((df == 0).sum())

#     # Only compute correlation for numeric columns
#     numeric_df = df.select_dtypes(include=[np.number])
#     if not numeric_df.empty:  # Check if there are any numeric columns
#         st.write("### Correlation Matrix")
#         st.write(numeric_df.corr())
#     else:
#         st.write("### Correlation Matrix")
#         st.write("No numeric columns to compute correlation.")

#     st.write("### Outliers")
#     for col in numeric_df.columns:
#         Q1 = df[col].quantile(0.25)
#         Q3 = df[col].quantile(0.75)
#         IQR = Q3 - Q1
#         outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))
#         st.write(f"{col}: {outliers.sum()} outliers")

# def clean_data(df, selected_operation):
#     if selected_operation == "Drop NA values":
#         df = df.dropna()

#     elif selected_operation == "Replace zeros":
#         zero_fill_option = st.selectbox("Choose fill method for zeros", ["mean", "median", "mode", "custom"])
#         if zero_fill_option == "custom":
#             zero_fill_value = st.text_input("Enter custom fill value for zeros")
#             df.replace(0, zero_fill_value, inplace=True)
#         else:
#             for col in df.columns:
#                 if (df[col] == 0).sum() > 0:
#                     if df[col].dtype in [np.number]:
#                         if zero_fill_option == "mean":
#                             df[col].replace(0, df[col].mean(), inplace=True)
#                         elif zero_fill_option == "median":
#                             df[col].replace(0, df[col].median(), inplace=True)
#                         elif zero_fill_option == "mode":
#                             df[col].replace(0, df[col].mode()[0], inplace=True)

#     elif selected_operation == "Fill NA values":
#         fill_option = st.selectbox("Choose fill method for NA values", ["mean", "median", "mode", "custom"])
#         if fill_option == "custom":
#             fill_value = st.text_input("Enter custom fill value for NA")
#             df.fillna(fill_value, inplace=True)
#         else:
#             for col in df.columns:
#                 if df[col].isnull().sum() > 0:
#                     if df[col].dtype in [np.number]:
#                         if fill_option == "mean":
#                             df[col].fillna(df[col].mean(), inplace=True)
#                         elif fill_option == "median":
#                             df[col].fillna(df[col].median(), inplace=True)
#                         elif fill_option == "mode":
#                             df[col].fillna(df[col].mode()[0], inplace=True)

#     elif selected_operation == "Drop duplicates":
#         df = df.drop_duplicates()

#     elif selected_operation == "Remove outliers":
#         for col in df.select_dtypes(include=[np.number]).columns:
#             Q1 = df[col].quantile(0.25)
#             Q3 = df[col].quantile(0.75)
#             IQR = Q3 - Q1
#             df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]

#     return df

if __name__ == "__main__":
    app()
