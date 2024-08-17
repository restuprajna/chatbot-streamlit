import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Load environment variables
gemini_api_key: str = os.environ.get("GEMINI_API_KEY")

# Function to generate a response using an external API
def generate_response(question: str) -> str:
    url = "http://127.0.0.1:8000/vertex-ai/{instance_id}/invoke"
    headers_template = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        "Authorization": "Bearer test",
    }
    data = {
        "input": question,
        "config": {},
        "kwargs": {}
    }
    response = requests.post(url, headers=headers_template, json=data)
    return json.loads(response.text)

# function to handle file upload
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        file_path = uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded and saved file: {file_path}")

# Initialize chat messages in session state
def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages
def display_chat_messages():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

# Handle chat input and response generation
def handle_chat_input():
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Generate and display assistant's response
        response = generate_response(question=prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

def file_manager():
    # Initialize session state for uploaded files
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    # Sidebar layout
    with st.sidebar:
        st.title("File Manager")

        # File uploader
        uploaded_file = st.file_uploader("Upload a file", type=None, label_visibility="visible")
        if uploaded_file is not None:
            st.session_state.uploaded_files.append(uploaded_file)

        # List all uploaded files
        st.subheader("Uploaded Files")
        if st.session_state.uploaded_files:
            for i, file in enumerate(st.session_state.uploaded_files):
                st.write(f"{i+1}. {file.name}")
        else:
            st.write("No files uploaded yet.")

        # Reset button to delete all uploaded files
        if st.button("Reset All Files"):
            st.session_state.uploaded_files.clear()
            st.success("All files have been deleted.")
            st.experimental_rerun()  # Refresh the app to update the file list

# Main app layout
def main():
    st.title("💬 Chatbot")

    # Initialize chat history
    initialize_chat()

    # Display chat messages
    display_chat_messages()

    # Chat input and response handling
    handle_chat_input()

    file_manager()

if __name__ == "__main__":
    main()