import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()

gemini_api_key: str=os.environ["GEMINI_API_KEY"]
st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])




def generate_response(question: str):
    url="http://127.0.0.1:8000/vertex-ai/{instance_id}/invoke"

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

    req_generate = requests.post(url, headers=headers_template, json=data)
    res_data = json.loads(req_generate.text)
    return res_data

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # client = OpenAI(api_key=gemini_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    response = generate_response(question=prompt)
    print(prompt)
    print(response)
    # msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)