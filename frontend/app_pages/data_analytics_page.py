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
    
    ### Features:
    - **Select Table**: Choose a table from the database to analyze.
    - **Prepare Data Insights**: Click the button to generate insights from the selected table.
    - **Correlation Matrix**: Visualize the correlation matrix of the selected table to understand the relationships between variables.
    - **Outliers Visualization**: View scatter plots of columns with outliers to understand their distribution.
    - **Density Plots**: View density plots to understand the distribution of data.
    
    Simply select a table and click 'Prepare data insights' to view the insights.
    """)

    # Fetching table names from the database
    # def get_table_names():
    #     conn_str = get_conn_str()
    #     with pyodbc.connect(conn_str) as conn:
    #         query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"
    #         tables = pd.read_sql(query, conn)
    #     return tables['TABLE_NAME'].tolist()

    # Fetching data from the selected table
    # def get_table_data(table_name):
    #     conn_str = get_conn_str()
    #     with pyodbc.connect(conn_str) as conn:
    #         df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    #     return df

    # Dropdown to select a table
    # table_name = st.selectbox("Choose a table", get_table_names())

    # Button to prepare data insights
    # if st.button("Prepare data insights"):
    #     df = get_table_data(table_name)
        
    #     # Exclude non-numerical columns
    #     numeric_df = df.select_dtypes(include=[np.number])
        
    #     # Compute and display the correlation matrix
    #     corr_matrix = numeric_df.corr()
    #     st.write("### Correlation Matrix")
        
    #     # Using seaborn to visualize the correlation matrix
    #     fig, ax = plt.subplots(figsize=(10, 8))
    #     sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    #     st.pyplot(fig)

    #     # Outliers Visualization using Z-scores and scatter plots
    #     st.write("### Outliers Visualization using Z-scores")
        
    #     numerical_cols = numeric_df.columns

    #     for x in numerical_cols:
    #         z_scores = np.abs((df[x] - df[x].mean()) / df[x].std())
    #         outliers = df[z_scores > 2]
            
    #         fig, ax = plt.subplots(figsize=(10, 5))
    #         ax.scatter(outliers[x], outliers[x], s=10, alpha=0.5, color='#3F5D7D')
    #         ax.set_title(x, fontsize=12)
    #         ax.set_xlabel(x, fontsize=10)
    #         ax.set_ylabel(x, fontsize=10)
    #         ax.tick_params(axis='both', which='major', labelsize=10, length=5)
    #         ax.spines['right'].set_visible(False)
    #         ax.spines['top'].set_visible(False)
            
    #         st.pyplot(fig)

    #     # Density Plots
    #     st.write("### Density Plots")
        
    #     for x in numerical_cols:
    #         fig, ax = plt.subplots(figsize=(10, 5))
    #         sns.kdeplot(df[x], ax=ax, shade=True, color='#3F5D7D')
    #         ax.set_title(x, fontsize=12)
    #         ax.set_xlabel('')
    #         ax.set_ylabel('')
    #         ax.tick_params(axis='both', which='major', labelsize=10, length=5)
    #         ax.spines['right'].set_visible(False)
    #         ax.spines['top'].set_visible(False)
            
    #         st.pyplot(fig)

if __name__ == "__main__":
    app()
