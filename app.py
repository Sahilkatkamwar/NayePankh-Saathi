from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from utils.db import init_db

load_dotenv()

st.set_page_config(
    page_title="NayePankh Saathi",
    page_icon="🪽",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

st.markdown(
    """
    <style>
    .hero {
        padding: 1.2rem 1.3rem;
        border-radius: 1.2rem;
        background: linear-gradient(135deg, rgba(46, 125, 255, 0.15), rgba(0,0,0,0));
        border: 1px solid rgba(255,255,255,0.08);
    }
    .small-muted {
        color: #a8b0bb;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom:0.2rem;">NayePankh Saathi</h1>
        <p class="small-muted" style="margin-top:0;">
            AI volunteer & awareness hub · Streamlit + Python
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("AI features", "3")
with c2:
    st.metric("Database", "SQLite")
with c3:
    st.metric("Deployment", "Streamlit Cloud")

st.subheader("What this app does")
st.write(
    "This app helps an NGO manage volunteer registration, answer common questions in English or Hindi, "
    "generate social awareness content, and view a simple impact dashboard."
)

st.subheader("Use the sidebar pages")
st.markdown(
    """
    - **Home** → project overview and architecture
    - **Register + AI match** → volunteer form plus AI role suggestion
    - **AI chatbot** → multilingual FAQ assistant
    - **Campaign generator** → Instagram / thread / email content
    - **Dashboard** → charts and volunteer analytics
    """
)
