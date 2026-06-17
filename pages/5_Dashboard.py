from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.db import (
    get_overview_stats,
    get_recent_volunteers,
    init_db,
    registrations_by_date,
    skills_distribution,
    program_distribution,
)

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

init_db()

st.title("Impact Dashboard")
st.write("View volunteer growth, skills, and program distribution.")

stats = get_overview_stats()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total volunteers", stats["total_volunteers"])
c2.metric("Unique cities", stats["unique_cities"])
c3.metric("Programs", stats["unique_programs"])
c4.metric("Skills tracked", stats["unique_skills"])

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Registrations over time")
    reg_data = pd.DataFrame(registrations_by_date())
    if not reg_data.empty:
        fig = px.line(reg_data, x="date", y="registrations", markers=True)
        fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No volunteer data yet.")

with right:
    st.subheader("Program distribution")
    program_data = pd.DataFrame(program_distribution())
    if not program_data.empty:
        fig = px.pie(program_data, names="preferred_program", values="count", hole=0.45)
        fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No volunteer data yet.")

st.subheader("Top skills")
skill_data = pd.DataFrame(skills_distribution())
if not skill_data.empty:
    fig = px.bar(skill_data, x="skill", y="count")
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No skills data yet.")

st.subheader("Recent volunteers")
search = st.text_input("Search by name, city, or email")
recent_df = pd.DataFrame(get_recent_volunteers(search=search, limit=25))

if not recent_df.empty:
    st.dataframe(recent_df, use_container_width=True)
else:
    st.info("No volunteer records found.")