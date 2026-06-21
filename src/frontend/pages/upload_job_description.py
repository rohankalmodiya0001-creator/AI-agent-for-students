import streamlit as st
from pathlib import Path

from frontend.services.api_client import load_json, post, save_json

DATA_DIR = Path("src/data")
JD_PATH = DATA_DIR / "uploaded_job_description.txt"
JD_PROFILE_PATH = DATA_DIR / "job_description_profile.json"


def render_upload_job_description() -> None:
    st.header("Upload Job Description")
    st.write("Paste the target job description text so the system can extract required skills, responsibilities, and keywords.")

    job_description_text = st.text_area("Job description text", height=300)
    if st.button("Save job description"):
        if job_description_text:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            JD_PATH.write_text(job_description_text, encoding="utf-8")
            st.success("Job description saved successfully.")
        else:
            st.warning("Please enter the job description text.")

    if JD_PATH.exists() and st.button("Analyze job description"):
        try:
            payload = {"job_description_text": JD_PATH.read_text(encoding="utf-8")}
            response = post("job-description", payload)
            save_json("job_description_profile.json", response["job_description_profile"])
            st.success("Job description analysis complete.")
            st.json(response["job_description_profile"])
        except Exception as error:
            st.error(f"Failed to analyze job description: {error}")

    jd_profile = load_json("job_description_profile.json")
    if jd_profile:
        st.subheader("Parsed Job Description Profile")
        st.json(jd_profile)
