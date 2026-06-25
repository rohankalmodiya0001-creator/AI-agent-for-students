import json
from pathlib import Path

import streamlit as st

from frontend.services.api_client import load_json, post, save_json

DATA_DIR = Path("src/data")
SKILL_GAP_REPORT_PATH = DATA_DIR / "skill_gap_report.json"


def render_skill_gap_analysis() -> None:
    st.header("Skill Gap Analysis")
    st.write("This page compares your resume with the job description to identify missing and weak skills.")

    resume_profile = load_json("resume_profile.json")
    jd_profile = load_json("job_description_profile.json")

    if not resume_profile or not jd_profile:
        st.warning("Please analyze both resume and job description first.")
        return

    if st.button("Run skill gap analysis"):
        try:
            payload = {
                "resume_profile": resume_profile,
                "job_description_profile": jd_profile,
            }
            response = post("skill-gap", payload)
            save_json("skill_gap_report.json", response["skill_gap_report"])
            st.success("Skill gap analysis complete.")
            st.rerun()
        except Exception as error:
            st.error(f"Failed to run skill gap analysis: {error}")

    report = load_json("skill_gap_report.json")
    if report:
        st.markdown("<br><hr style='opacity: 0.15;'><br>", unsafe_allow_html=True)
        st.subheader("📊 Skill Gap Analysis Results")
        
        # Display Match & Readiness Metrics in columns
        cols = st.columns(2)
        match_score = report.get("match_score", 0)
        readiness_score = report.get("readiness_score", 0)
        
        with cols[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Match Score")
            st.markdown(f'<h2 style="color:#10b981; margin:0.5rem 0;">{match_score:.1f}%</h2>', unsafe_allow_html=True)
            st.progress(match_score / 100.0)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with cols[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 Readiness Score")
            st.markdown(f'<h2 style="color:#6366f1; margin:0.5rem 0;">{readiness_score:.1f}%</h2>', unsafe_allow_html=True)
            st.progress(readiness_score / 100.0)
            st.markdown('</div>', unsafe_allow_html=True)

        # Summary card
        st.markdown('<div class="custom-card status-card-info">', unsafe_allow_html=True)
        st.markdown("#### 📝 Executive Summary")
        st.write(report.get("summary", "No summary available."))
        st.markdown('</div>', unsafe_allow_html=True)

        # Detailed columns for Strengths, Weaknesses, and Gaps
        cols_details = st.columns(3)
        with cols_details[0]:
            st.markdown('<div class="custom-card status-card-success" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("#### 🟢 Strengths")
            strengths = report.get("strengths", [])
            if strengths:
                pill_html = "".join([f'<span class="pill-badge pill-badge-green">{item}</span>' for item in strengths])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No strong areas identified.*")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with cols_details[1]:
            st.markdown('<div class="custom-card status-card-warning" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("#### 🟡 Weak Skills")
            weak_skills = report.get("weak_skills", [])
            if weak_skills:
                pill_html = "".join([f'<span class="pill-badge pill-badge-yellow">{item}</span>' for item in weak_skills])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No weak skills identified.*")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with cols_details[2]:
            st.markdown('<div class="custom-card status-card-danger" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("#### 🔴 Missing Skills")
            missing_skills = report.get("missing_skills", [])
            if missing_skills:
                pill_html = "".join([f'<span class="pill-badge pill-badge-red">{item}</span>' for item in missing_skills])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No missing skills identified.*")
            st.markdown('</div>', unsafe_allow_html=True)

