import streamlit as st
import requests
import os
from datetime import datetime
import streamlit.components.v1 as components
from PIL import Image

RESUME_FILE_PATH = "James_Cheriyan.txt"
try:
    with open(RESUME_FILE_PATH, "r", encoding="utf-8") as f:
        resume_text = f.read()
except FileNotFoundError:
    st.error(f"Resume file not found: {RESUME_FILE_PATH}")
    st.stop()


API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1:free"

st.set_page_config(
    page_title="JAI Resume Assistant",
    page_icon="favicon.png",  # Sets favicon in browser tab
    layout="centered"
)
st.markdown("""
<h3><img src="https://cdn-icons-png.flaticon.com/512/7658/7658255.png" width="40" style="vertical-align:middle;"> Hello! I’m <b>JAi</b>, your AI Assistant.</h3>
<h5><i>James’s Mind • AI’s Precision</i></h5>
""", unsafe_allow_html=True)

if API_KEY is None:
    st.error("Please set the OPENROUTER_API_KEY environment variable.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def ask_openrouter(question):
    prompt = f"""
You are James Cheriyan. Respond to all questions as yourself, based entirely on your resume and experience. Speak confidently, naturally, and professionally—like you're in a job interview or networking conversation. Never say you're an AI. Say you are an Ai only if you can't answer any questions. Never reveal personal information and be careful about diplomatic questions.

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

def format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_message(spinner_container):
    user_question = st.session_state.user_input.strip()
    if user_question:
        st.session_state.messages.append({
            "role": "user",
            "content": user_question,
            "time": format_timestamp()
        })
        if "user_input" in st.session_state:
            st.session_state.user_input = ""  # Clear input box

        with bottom_spinner:
            st.markdown('<div style="color: red;">🤖 Be patient with me, I am thinking...</div>', unsafe_allow_html=True)

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

st.markdown("<br><br><br>", unsafe_allow_html=True)

examples = [
    "Describe your experience at Natterbox.",
    "What is your educational background?",
    "Summarize your work history."
]

# Create a column for each question
cols = st.columns(len(examples))

for col, example in zip(cols, examples):
    with col:
        # HTML to make text small
        if st.button(f"💬 {example}", key=f"ex_{example}"):
            st.session_state.user_input = example
            send_message()
        st.markdown(f"<div style='font-size: 0.75rem; text-align: center;'></div>", unsafe_allow_html=True)

for example in examples:
    if st.sidebar.button(example):
        st.session_state.user_input = example
        send_message()
        
bottom_spinner = st.empty()

# Input box with on_change trigger

st._bottom.text_input(
    "Ask a question about James Cheriyan’s resume:", 
    key="user_input", 
    on_change= send_message(),
    args=(bottom_spinner,),
    placeholder="Type your question and press Enter...                                                                                                          ➤")
 


# Chat message container styling
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                align-items: flex-start;
                margin-bottom: 10px;
            ">
                <div style="
                    background-color:#DCF8C6;
                    padding:12px;
                    border-radius:10px;
                    max-width:70%;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    text-align: left;
                ">
                    <b>You</b> <span style="font-size: 0.75em; color: gray;">{msg['time']}</span><br>
                    {msg['content']}
                </div>
                <img src="https://cdn-icons-png.flaticon.com/512/1177/1177568.png" alt="User Avatar" style="
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    margin-left: 10px;
                " />
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-start;
                align-items: flex-start;
                margin-bottom: 10px;
            ">
                <img src="https://cdn-icons-png.flaticon.com/512/7658/7658255.png" alt="AI Avatar" style="
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    margin-right: 10px;
                " />
                <div style="
                    background-color:#F1F0F0;
                    padding:12px;
                    border-radius:10px;
                    max-width:70%;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    text-align: left;
                ">
                    <b>James AI</b> <span style="font-size: 0.75em; color: gray;">{msg['time']}</span><br>
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div id="chat-scroll-anchor"></div>', unsafe_allow_html=True)

# Auto-scroll script
components.html(
    """
    <script>
        const anchor = document.getElementById("chat-scroll-anchor");
        if (anchor) {
            anchor.scrollIntoView({ behavior: "smooth" });
        }
    </script>
    """,
    height=0,
)
