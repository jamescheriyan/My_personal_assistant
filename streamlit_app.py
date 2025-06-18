import streamlit as st
import requests
import os
from datetime import datetime

API_KEY = "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"
MODEL = "deepseek/deepseek-r1:free"

st.set_page_config(page_title="AI Resume Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI Resume Assistant")

if API_KEY is None:
    st.error("Please set the OPENROUTER_API_KEY environment variable.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def ask_openrouter(question):
    prompt = f"""
You are James Cheriyan. Answer questions based only on the resume below, in a professional, natural style.

Resume:
\"\"\"{resume_text}\"\"\"

Question: {question}
"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

resume_text = """
James Cheriyan is a dedicated technical support professional with experience in troubleshooting, system monitoring, and customer support.
"""

def format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_message():
    user_question = st.session_state.user_input.strip()
    if user_question:
        st.session_state.messages.append({
            "role": "user",
            "content": user_question,
            "time": format_timestamp()
        })
        st.session_state.user_input = ""  # Clear input box

        with st.spinner("🤖 Thinking..."):
            answer = ask_openrouter(user_question)
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "time": format_timestamp()
        })

# Sidebar example questions
st.sidebar.header("Example questions")
examples = [
    "What are your technical skills?",
    "Describe your experience at Natterbox.",
    "What is your educational background?",
    "Summarize your work history.",
    "What experience do you have in telecom or VoIP?",
]

for example in examples:
    if st.sidebar.button(example):
        st.session_state.user_input = example
        send_message()

# Input box with on_change trigger
st.sidebar.text_input(
    "Ask a question about James Cheriyan’s resume:", 
    key="user_input", 
    on_change=send_message,
    placeholder="Type your question and press Enter..."
)


# Chat message container styling
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#DCF8C6;
                padding:12px;
                border-radius:10px;
                max-width:70%;
                margin-left:auto;
                margin-bottom:8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                <b>You</b> <span style="font-size: 0.75em; color: gray;">{msg['time']}</span><br>
                {msg['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#F1F0F0;
                padding:12px;
                border-radius:10px;
                max-width:70%;
                margin-right:auto;
                margin-bottom:8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                <b>Assistant</b> <span style="font-size: 0.75em; color: gray;">{msg['time']}</span><br>
                {msg['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )