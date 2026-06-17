from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List

import google.generativeai as genai
import streamlit as st

MODEL_NAME = "gemini-2.5-pro"


def get_api_key() -> str:
    key = ""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GEMINI_API_KEY", "")


def get_model():
    api_key = get_api_key()
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


def generate_text(prompt: str, temperature: float = 0.4, max_output_tokens: int = 1024) -> str:
    model = get_model()
    if model is None:
        return ""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            },
        )
        return (response.text or "").strip()
    except Exception as exc:
        return f"AI error: {exc}"


def _extract_json(text: str) -> Dict[str, Any] | None:
    if not text:
        return None

    fenced = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        text = fenced.group(1)

    try:
        return json.loads(text.strip())
    except Exception:
        return None


def _fallback_role_matches(profile: Dict[str, Any]) -> Dict[str, Any]:
    skills_text = (profile.get("skills") or "").lower()
    role_text = (profile.get("preferred_role") or "").lower()
    program_text = (profile.get("preferred_program") or "").lower()

    role_map = [
        ("school outreach", ["teaching", "communication", "english", "hindi", "public speaking"]),
        ("event support", ["event management", "coordination", "leadership"]),
        ("social media", ["social media", "writing", "canva", "design"]),
        ("teaching / mentoring", ["teaching", "communication", "english", "hindi"]),
        ("design / content", ["canva", "design", "video editing", "writing"]),
        ("fundraising", ["communication", "public speaking", "leadership"]),
        ("data entry / admin", ["excel", "data analysis", "coordination"]),
        ("field support", ["leadership", "coordination", "communication"]),
    ]

    scored = []
    for role, keywords in role_map:
        score = 30
        reasons = []
        if role == role_text:
            score += 25
            reasons.append("matches the preferred role")
        if program_text and any(k in program_text for k in ["education", "awareness", "community", "all"]):
            score += 10
        hits = [k for k in keywords if k in skills_text]
        score += len(hits) * 10
        if hits:
            reasons.append("skills match: " + ", ".join(hits))
        scored.append(
            {
                "role": role.title(),
                "score": min(score, 99),
                "reason": "; ".join(reasons) if reasons else "good general fit",
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)

    return {
        "summary": "This is a fallback match because the Gemini API key is missing or the AI call failed.",
        "top_matches": scored[:3],
        "next_steps": [
            "Review the top role and contact the volunteer for onboarding.",
            "Assign a small first task to confirm fit.",
            "Update the volunteer record after the first activity.",
        ],
    }


def match_volunteer(profile: Dict[str, Any]) -> Dict[str, Any]:
    model = get_model()
    if model is None:
        return _fallback_role_matches(profile)

    prompt = f"""
You are helping an NGO match a volunteer to the best role.

Return ONLY valid JSON with this structure:
{{
  "summary": "short explanation",
  "top_matches": [
    {{"role": "Role name", "score": 0-100, "reason": "why this fits"}},
    {{"role": "Role name", "score": 0-100, "reason": "why this fits"}},
    {{"role": "Role name", "score": 0-100, "reason": "why this fits"}}
  ],
  "next_steps": ["step 1", "step 2", "step 3"]
}}

Volunteer profile:
Name: {profile.get("full_name", "")}
City: {profile.get("city", "")}
Age: {profile.get("age", "")}
Preferred program: {profile.get("preferred_program", "")}
Preferred role: {profile.get("preferred_role", "")}
Skills: {profile.get("skills", "")}
Availability: {profile.get("availability", "")}
Motivation: {profile.get("motivation", "")}

Rules:
- Be practical and concise.
- Match the volunteer to NGO work.
- Prefer roles that fit the skills and preferred role.
- Output must be JSON only.
"""

    try:
        raw = generate_text(prompt, temperature=0.3, max_output_tokens=900)
        parsed = _extract_json(raw)
        return parsed if parsed else _fallback_role_matches(profile)
    except Exception:
        return _fallback_role_matches(profile)


def faq_chat(
    question: str,
    context: str,
    history: List[Dict[str, str]],
    language: str = "English",
) -> str:
    model = get_model()
    if model is None:
        return _faq_fallback(question, context, language)

    history_text = "\n".join([f'{m["role"]}: {m["content"]}' for m in history[-8:]])

    prompt = f"""
You are the NayePankh Saathi FAQ assistant.
Answer only using the context below.
If the answer is not available, say that you could not find it in the FAQ and suggest contacting the NGO admin team.

Reply language: {language}

FAQ context:
{context}

Conversation so far:
{history_text}

User question:
{question}

Write a friendly, clear answer in {language}.
"""

    try:
        reply = generate_text(prompt, temperature=0.3, max_output_tokens=500)
        return reply or _faq_fallback(question, context, language)
    except Exception:
        return _faq_fallback(question, context, language)


def _faq_fallback(question: str, context: str, language: str) -> str:
    q = question.lower()
    if "volunteer" in q or "volunte" in q:
        return "Fill the registration form on the Register page, and the team can review your skills and availability."
    if "hindi" in q:
        return "Yes, the assistant supports Hindi and English."
    if language.lower() == "hindi":
        return "Aap Register page par form bhariye. Team aapke skills ke hisaab se best role suggest karegi."
    return "Please check the Register page to submit your details. The NGO team can then review your profile and contact you."


def generate_campaign_copy(
    campaign_goal: str,
    audience: str,
    platform: str,
    tone: str,
    language: str,
    key_message: str,
    call_to_action: str,
) -> Dict[str, str] | str:
    model = get_model()
    if model is None:
        return {
            "instagram_post": f"{campaign_goal}\n\nAudience: {audience}\n\n{key_message}\n\n{call_to_action}",
            "twitter_thread": f"1/ {campaign_goal}\n2/ {key_message}\n3/ {call_to_action}",
            "email_draft": f"Subject: {campaign_goal}\n\nHi,\n\n{key_message}\n\n{call_to_action}\n",
            "hashtags": "#NayePankhSaathi #Volunteer #Awareness",
        }

    prompt = f"""
Create campaign content for an NGO.

Return ONLY valid JSON with this structure:
{{
  "instagram_post": "caption",
  "twitter_thread": "numbered thread",
  "email_draft": "short email",
  "hashtags": "#tag1 #tag2 #tag3"
}}

Campaign goal: {campaign_goal}
Audience: {audience}
Platform: {platform}
Tone: {tone}
Language: {language}
Key message: {key_message}
Call to action: {call_to_action}

Rules:
- Keep it practical and social-media friendly.
- Make the Instagram post engaging.
- Make the thread concise and readable.
- Make the email clear and professional.
- Output JSON only.
"""

    try:
        raw = generate_text(prompt, temperature=0.5, max_output_tokens=1000)
        parsed = _extract_json(raw)
        return parsed if parsed else {
            "instagram_post": raw,
            "twitter_thread": raw,
            "email_draft": raw,
            "hashtags": "#NayePankhSaathi",
        }
    except Exception as exc:
        return {"instagram_post": f"AI error: {exc}", "twitter_thread": "", "email_draft": "", "hashtags": ""}