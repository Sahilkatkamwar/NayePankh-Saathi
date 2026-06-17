from __future__ import annotations

import streamlit as st

from utils.ai import faq_chat
from utils.db import init_db

st.set_page_config(
    page_title="AI chatbot",
    page_icon="💬",
    layout="wide",
)

init_db()

st.title("AI FAQ Chatbot")
st.write("Ask questions in English or Hindi about the NGO and its programs.")

FAQ_CONTEXT = """
NayePankh is an NGO focused on community support, volunteer engagement, education help,
awareness campaigns, and outreach programs.

Common questions and answers:
- What does the NGO do? It supports education, awareness, and community outreach.
- How can I volunteer? Fill the registration form and the team will contact you.
- What skills are useful? Communication, teaching, design, social media, and coordination.
- Is Hindi supported? Yes, the assistant should reply in Hindi or English depending on the user.
- How do campaigns help? They improve awareness on Instagram, X/Twitter, and email.
- Who should I contact? Ask the NGO admin team after registration.
"""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

language = st.selectbox("Reply language", ["English", "Hindi"], index=0)

with st.expander("Suggested questions", expanded=False):
    st.write("• How can I volunteer?")
    st.write("• What work does the NGO do?")
    st.write("• Mujhe volunteer kaise banna hai?")
    st.write("• What skills are useful?")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_query = st.chat_input("Type your question here...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = faq_chat(
                question=user_query,
                context=FAQ_CONTEXT,
                history=st.session_state.chat_history,
                language=language,
            )
        st.write(reply)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})