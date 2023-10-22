import streamlit as st
import httpx

def app():
    st.title("🤖 AI Assistant")

    user_input = st.text_input("You: ", "")
    if st.button("Send"):
        with httpx.Client() as client:
            response = client.post("http://backend:8000/chat/", json={"user_input": user_input})
        if response.status_code == 200:
            model_output = response.json()["model_output"]
            st.write(f"AI: {model_output}")
        else:
            st.write("Error: Unable to get a response.")

    st.write("Chat history:")