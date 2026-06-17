from __future__ import annotations

import streamlit as st

from utils.ai import generate_campaign_copy
from utils.db import init_db

st.set_page_config(
    page_title="Campaign generator",
    page_icon="📣",
    layout="wide",
)

init_db()

st.title("Campaign Generator")
st.write("Generate social content for an awareness campaign in one click.")

col1, col2 = st.columns(2)

with col1:
    campaign_goal = st.text_input("Campaign goal", value="Promote volunteer registration")
    audience = st.text_input("Target audience", value="College students and young professionals")
    platform = st.selectbox("Primary platform", ["Instagram", "X / Twitter", "Email", "All"])
    tone = st.selectbox("Tone", ["Friendly", "Formal", "Inspirational", "Urgent"])
    language = st.selectbox("Output language", ["English", "Hindi", "Bilingual"])

with col2:
    key_message = st.text_area(
        "Key message",
        value="Invite people to support the NGO and join as volunteers.",
        height=130,
    )
    call_to_action = st.text_input("Call to action", value="Register now and join the mission")

generate = st.button("Generate content")

if generate:
    with st.spinner("Creating campaign copy..."):
        result = generate_campaign_copy(
            campaign_goal=campaign_goal,
            audience=audience,
            platform=platform,
            tone=tone,
            language=language,
            key_message=key_message,
            call_to_action=call_to_action,
        )

    st.subheader("Campaign output")

    if isinstance(result, dict):
        tab1, tab2, tab3, tab4 = st.tabs(["Instagram post", "Thread", "Email draft", "Hashtags"])

        with tab1:
            st.text_area("Instagram post", result.get("instagram_post", ""), height=220)
        with tab2:
            st.text_area("X / Twitter thread", result.get("twitter_thread", ""), height=220)
        with tab3:
            st.text_area("Email draft", result.get("email_draft", ""), height=220)
        with tab4:
            st.code(result.get("hashtags", ""), language="text")

        st.download_button(
            "Download content as text",
            data="\n\n".join(
                [
                    "INSTAGRAM POST\n" + result.get("instagram_post", ""),
                    "TWITTER THREAD\n" + result.get("twitter_thread", ""),
                    "EMAIL DRAFT\n" + result.get("email_draft", ""),
                    "HASHTAGS\n" + result.get("hashtags", ""),
                ]
            ),
            file_name="naye_pankh_campaign.txt",
            mime="text/plain",
        )
    else:
        st.write(result)