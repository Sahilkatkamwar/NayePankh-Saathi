from __future__ import annotations

from datetime import datetime

import streamlit as st

from utils.ai import match_volunteer
from utils.db import add_volunteer, init_db

st.set_page_config(
    page_title="Register + AI match",
    page_icon="📝",
    layout="wide",
)

init_db()

st.title("Volunteer Registration + AI Match")
st.write("Register a volunteer and let the app suggest the best-fit NGO role.")

role_options = [
    "School outreach",
    "Event support",
    "Social media",
    "Teaching / mentoring",
    "Design / content",
    "Fundraising",
    "Data entry / admin",
    "Field support",
]

skill_options = [
    "Communication",
    "Leadership",
    "Teaching",
    "Canva / design",
    "Writing",
    "Social media",
    "Photography",
    "Video editing",
    "Public speaking",
    "Hindi",
    "English",
    "Excel",
    "Data analysis",
    "Event management",
    "Coordination",
]

with st.form("volunteer_form"):
    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full name")
        email = st.text_input("Email")
        phone = st.text_input("Phone number")
        age = st.number_input("Age", min_value=10, max_value=100, value=18)

    with col2:
        city = st.text_input("City")
        preferred_program = st.selectbox(
            "Preferred program",
            [
                "Education support",
                "Awareness campaign",
                "Community outreach",
                "Fundraising",
                "All programs",
            ],
        )
        preferred_role = st.selectbox("Preferred role", role_options)
        availability = st.selectbox(
            "Availability",
            ["Weekdays", "Weekends", "Evenings", "Flexible"],
        )

    skills = st.multiselect("Skills", skill_options)
    motivation = st.text_area("Why do you want to volunteer?", height=120)

    submitted = st.form_submit_button("Submit registration")

if submitted:
    if not full_name or not email or not city:
        st.error("Please fill the required fields: full name, email, and city.")
        st.stop()

    record = {
        "full_name": full_name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "age": int(age),
        "city": city.strip(),
        "preferred_program": preferred_program,
        "preferred_role": preferred_role,
        "skills": ", ".join(skills),
        "availability": availability,
        "motivation": motivation.strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    volunteer_id = add_volunteer(record)
    st.success(f"Volunteer registered successfully. Record ID: {volunteer_id}")

    with st.spinner("Finding the best role match..."):
        match_result = match_volunteer(record)

    st.subheader("AI match result")

    if isinstance(match_result, dict):
        summary = match_result.get("summary", "")
        top_matches = match_result.get("top_matches", [])
        next_steps = match_result.get("next_steps", [])

        if summary:
            st.info(summary)

        if top_matches:
            for item in top_matches:
                role = item.get("role", "Role")
                score = item.get("score", "")
                reason = item.get("reason", "")
                st.markdown(f"**{role}** — {score}")
                st.write(reason)

        if next_steps:
            st.markdown("### Next steps")
            for step in next_steps:
                st.write(f"- {step}")
    else:
        st.write(match_result)

    st.divider()
    st.caption("The volunteer record has been saved in SQLite.")