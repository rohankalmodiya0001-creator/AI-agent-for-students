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
        st.subheader("Recommended Learning Steps")
        for step in roadmap:
            st.markdown(f"- {step}")
