import json
from pathlib import Path

import streamlit as st

from frontend.services.api_client import load_json, post, save_json


def render_learning_roadmap() -> None:
    st.header("Learning Roadmap")
    st.write("The roadmap synthesizes missing and weak skills into an adaptive study plan.")

    skill_gap_report = load_json("skill_gap_report.json")
    roadmap_path = Path("src/data/roadmap.json")

    if not skill_gap_report:
        st.info("Run skill gap analysis first to generate the roadmap.")
        return

    if st.button("Generate roadmap"):
        try:
            response = post("roadmap", {"skill_gap_report": skill_gap_report})
            save_json("roadmap.json", response["roadmap"])
            st.success("Learning roadmap generated successfully.")
            st.rerun()
        except Exception as error:
            st.error(f"Failed to generate roadmap: {error}")
            return

    if roadmap_path.exists():
        roadmap = json.loads(roadmap_path.read_text(encoding="utf-8"))
        st.markdown("<br><hr style='opacity: 0.15;'><br>", unsafe_allow_html=True)
        st.subheader("🏁 Recommended Learning Steps")
        
        # Timeline wrapper
        st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)
        for idx, step in enumerate(roadmap):
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-step">Step {idx + 1}</div>
                    <div class="custom-card" style="margin-top:0.25rem; margin-bottom:0; padding: 1.2rem;">
                        {step}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

