import streamlit as st
import requests
import os
from datetime import datetime
import streamlit.components.v1 as components
from PIL import Image


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

resume_text = """
JAMES CHERIYAN  
Technical Support Specialist | IT Solutions | Customer Experience  
📞 +44 7442585688  
📧 jamescheriyan47@outlook.com  
📍 Belfast, UK  

---

🧾 PROFESSIONAL SUMMARY  
Dedicated technical support professional with a proven track record in troubleshooting and technical problem resolution across various platforms. Passionate about enhancing customer experience through effective communication and proactive problem-solving. Experienced in 24x7 environments, system monitoring, and cross-team collaboration. Skilled in identifying customer needs and implementing process improvements that build trust and satisfaction.

---

🛠️ TECHNICAL SKILLS  
- Technical Troubleshooting  
- System Monitoring  
- Problem Solving  
- Collaboration  
- Communication Skills  
- Attention to Detail  
- Process Optimization  
- 24x7 Environment  
- Adaptability  
- Telecoms Experience  
- Quick Learning  
- Networking Knowledge  
- Decision Making  
- Help Desk  
- Active Listening  
- User Feedback Analysis  
- CRM Proficiency  
- Knowledge Base Development  
- VoIP  
- Python  
- IT Systems Proficiency  
- SQL  

---

🏆 STRENGTHS  
- Excels in software support via multiple channels  
- Strong cross-functional collaboration  
- Customer-focused problem solver  
- Effective communicator  
- Analytical thinker with a customer-centric mindset  

---

💼 WORK EXPERIENCE  

**Technical Support Engineer**  
*Natterbox* — Belfast, UK  
📅 Jan 2025 – Present  

**Customer Contact & Experience Specialist**  
*NatWest Group via FirstSource* — Belfast, UK  
📅 Mar 2022 – Present  
- First point of contact for online banking issues via call and email  
- Documented frequent issues and solutions  
- Collaborated with IT to resolve tech issues  
- Assisted with digital banking service adoption  
- Monitored systems to ensure seamless operations  
- Suggested recurring problem process improvements  
- Maintained detailed logs for analysis  

**Customer Contact Associate - Technical Support**  
*Comcast Corp Xfinity via Nuance Communications* — Bangalore  
📅 Jul 2019 – Sep 2021  
- Provided tech support via chat, email, CRM  
- Diagnosed system failures in time-sensitive settings  
- Monitored networks and resolved bottlenecks  
- Supported digital services (internet, TV, VoIP)  
- Implemented process improvements  
- Maintained CRM records  
- Acted as liaison between tech teams and users  

**Customer Service Advisor - Technical Support**  
*AT&T U-verse via [24]7.ai* — Bangalore  
📅 Nov 2017 – Dec 2018  
- Managed live chat/email/CRM in 24x7 environment  
- Resolved issues for AT&T U-verse services  
- Ensured quality compliance and procedure adherence  
- Delivered tech support training to teams  
- Maintained accurate CRM records  
- Assisted customers with setups and upgrades  

**IT Technical Support Specialist and Trainer**  
*Little Flower Convent School*  
📅 Jun 2014 – Jan 2017  
- Trained staff on TechNext systems  
- Supported school software and improved usability  
- Helped over 300 students improve computer skills, increasing pass rates by 95%  

---

🎓 EDUCATION  

**MSc Computer Science**  
Ulster University — Belfast, UK  
📅 Feb 2022 – Sep 2023  

**BCA – Bachelor’s in Computer Application**  
Kannur University — Kannur, India  
📅 Jun 2011 – Jun 2014  

---

🎯 HOBBIES  
- Football  
- Badminton  
- Cycling  
- Traveling & Hiking  
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
        if "user_input" in st.session_state:
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

# Input box with on_change trigger

st._bottom.text_input(
    "Ask a question about James Cheriyan’s resume:", 
    key="user_input", 
    on_change=send_message,
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
