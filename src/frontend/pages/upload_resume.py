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
        st.markdown("<br><hr style='opacity: 0.15;'><br>", unsafe_allow_html=True)
        st.subheader("📝 Parsed Resume Profile")
        
        # Grid layout for Skills & Technologies
        cols = st.columns(2)
        with cols[0]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🛠️ Core Skills")
            skills = resume_profile.get("skills", [])
            if skills:
                # Group pills in a container
                pill_html = "".join([f'<span class="pill-badge">{skill}</span>' for skill in skills])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No skills parsed.*")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with cols[1]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 💻 Technologies & Frameworks")
            techs = resume_profile.get("technologies", [])
            if techs:
                pill_html = "".join([f'<span class="pill-badge pill-badge-green">{tech}</span>' for tech in techs])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No technologies parsed.*")
            st.markdown('</div>', unsafe_allow_html=True)

        # Experience & Projects & Certifications
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 💼 Experience Summary")
        exp = resume_profile.get("experience", "")
        if exp:
            st.write(exp)
        else:
            st.write("*No work experience details parsed.*")
        st.markdown('</div>', unsafe_allow_html=True)

        cols2 = st.columns(2)
        with cols2[0]:
            st.markdown('<div class="custom-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("#### 🚀 Projects")
            projects = resume_profile.get("projects", [])
            if projects:
                for proj in projects:
                    st.markdown(f"**•** {proj}")
            else:
                st.write("*No projects parsed.*")
            st.markdown('</div>', unsafe_allow_html=True)

        with cols2[1]:
            st.markdown('<div class="custom-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("#### 📜 Certifications & Achievements")
            certs = resume_profile.get("certifications", [])
            if certs:
                pill_html = "".join([f'<span class="pill-badge pill-badge-yellow">{cert}</span>' for cert in certs])
                st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
            else:
                st.write("*No certifications parsed.*")
            st.markdown('</div>', unsafe_allow_html=True)

