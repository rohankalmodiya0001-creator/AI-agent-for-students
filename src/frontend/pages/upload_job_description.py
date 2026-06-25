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
        st.markdown("<br><hr style='opacity: 0.15;'><br>", unsafe_allow_html=True)
        st.subheader("🎯 Parsed Job Description Profile")
        
        # Grid layout for Seniority level & Keywords
        cols = st.columns(2)
        with cols[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🎖️ Target Seniority Level")
            level = jd_profile.get("seniority_level", "Not specified")
            st.markdown(f'<h3 style="color:#6366f1; margin-top:0.5rem; margin-bottom:0;">{level}</h3>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with cols[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🔑 Key Job Keywords")
            kws = jd_profile.get("keywords", [])
            if kws:
                pill_html = "".join([f'<span class="pill-badge pill-badge-yellow">{kw}</span>' for kw in kws])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No keywords parsed.*")
            st.markdown('</div>', unsafe_allow_html=True)

        cols2 = st.columns(2)
        with cols2[0]:
            st.markdown('<div class="custom-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("#### 🛠️ Required Core Skills")
            req_skills = jd_profile.get("required_skills", [])
            if req_skills:
                pill_html = "".join([f'<span class="pill-badge">{skill}</span>' for skill in req_skills])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No required skills specified.*")
            st.markdown('</div>', unsafe_allow_html=True)

        with cols2[1]:
            st.markdown('<div class="custom-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("#### 💻 Target Technologies & Frameworks")
            techs = jd_profile.get("technologies", [])
            if techs:
                pill_html = "".join([f'<span class="pill-badge pill-badge-green">{tech}</span>' for tech in techs])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No technologies parsed.*")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Key Responsibilities")
        resps = jd_profile.get("responsibilities", [])
        if resps:
            for resp in resps:
                st.markdown(f"**•** {resp}")
        else:
            st.write("*No responsibilities listed.*")
        st.markdown('</div>', unsafe_allow_html=True)

