import streamlit as st

from utils.utils import api_request, get_headers

def app():
    st.title("💬 AI Assistant")
    headers = get_headers()

    # Initialize or get the existing chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You: ", "")
    if st.button("Send"):
        response = api_request("http://backend:8000/chat/", "POST", json={"user_input": user_input}, headers=headers)
        if response.status_code == 200:
            llm_output = response.json()["llm_output"]
            st.session_state.chat_history.append({"role": "You", "message": user_input})
            st.session_state.chat_history.append({"role": "AI", "message": llm_output})
        else:
            st.write("Error: Unable to get a response.")

    # Display chat history with the latest message on top
    for chat in reversed(st.session_state.chat_history):
        st.write(f"{chat['role']}: {chat['message']}")
    
    if st.button("Delete history"):
        # Clear the chat history in the Streamlit session
        st.session_state.chat_history.clear()

        # Make an HTTP request to delete the user's history from the database
        response = api_request("http://backend:8000/chat_history/", "DELETE")  # TODO: Implement logic for only deleting a single user's history
        
        if response.status_code == 200:
            st.write("Successfully deleted chat history.")
        else:
            st.write("Failed to delete chat history.")

if __name__ == "__main__":
    app()