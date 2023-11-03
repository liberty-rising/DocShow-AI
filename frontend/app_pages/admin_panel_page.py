import httpx
import streamlit as st


def app():
    st.title("⚙️ Admin Panel")

    st.subheader("Table management")
    with httpx.Client() as client:
        tables = client.get("http://backend:8000/tables/").json()

    selected_table = st.selectbox('Choose a table to drop:', tables)
    
    if st.button("Drop Table"):
        with httpx.Client() as client:
            response = client.delete("http://backend:8000/table/", params={"table_name":selected_table})
        
        if response.status_code == 200:
            st.write(f"Successfully dropped table {selected_table}.")
        else:
            st.write(f"Failed to drop table {selected_table}.")

if __name__ == "__main__":
    app()