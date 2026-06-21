import streamlit as st
from pathlib import Path

from frontend.services.api_client import load_json, post, save_json

DATA_DIR = Path("src/data")
RESUME_PATH = DATA_DIR / "uploaded_resume.pdf"
RESUME_PROFILE_PATH = DATA_DIR / "resume_profile.json"


def render_upload_resume() -> None:
    st.header("Upload Resume")
    st.write("Upload your resume PDF to extract skills, projects, experience, certifications, and technologies.")

    uploaded_file = st.file_uploader("Choose a resume PDF", type=["pdf"])
    if uploaded_file is not None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with RESUME_PATH.open("wb") as file:
            file.write(uploaded_file.getbuffer())
        st.success("Resume uploaded successfully.")
        st.write("Resume path:", str(RESUME_PATH))

    if RESUME_PATH.exists() and st.button("Analyze resume"):
        try:
            payload = {"resume_path": str(RESUME_PATH)}
            response = post("resume", payload)
            save_json("resume_profile.json", response["resume_profile"])
            st.success("Resume analysis complete.")
            st.json(response["resume_profile"])
        except Exception as error:
            st.error(f"Failed to analyze resume: {error}")

    resume_profile = load_json("resume_profile.json")
    if resume_profile:
        st.subheader("Parsed Resume Profile")
        st.json(resume_profile)
