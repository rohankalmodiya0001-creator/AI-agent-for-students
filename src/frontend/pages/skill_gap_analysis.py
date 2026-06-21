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
            st.json(response["skill_gap_report"])
        except Exception as error:
            st.error(f"Failed to run skill gap analysis: {error}")

    report = load_json("skill_gap_report.json")
    if report:
        st.subheader("Skill Gap Report")
        st.json(report)
        st.write("### Summary")
        st.write(report.get("summary", "No summary available."))
