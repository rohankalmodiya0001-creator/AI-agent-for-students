"""Streamlit application shell for the Multi-Agent RAG Interview Coach."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from frontend.pages.evaluation_dashboard import render_evaluation_dashboard
from frontend.pages.final_report import render_final_report
from frontend.pages.home import render_home
from frontend.pages.interview_history import render_interview_history
from frontend.pages.knowledge_base import render_knowledge_base
from frontend.pages.learning_roadmap import render_learning_roadmap
from frontend.pages.memory_dashboard import render_memory_dashboard
from frontend.pages.mock_interview import render_mock_interview
from frontend.pages.skill_gap_analysis import render_skill_gap_analysis
from frontend.pages.upload_job_description import render_upload_job_description
from frontend.pages.upload_resume import render_upload_resume


def _render_styles() -> None:
    st.markdown(
        """
        <style>
            .block-container { padding-top: 1.5rem; }
            .hero {
                background: linear-gradient(135deg, #0F4C81 0%, #1B6CA8 45%, #E8EEF5 100%);
                color: #FFFFFF;
                border-radius: 24px;
                padding: 2rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 18px 50px rgba(15, 76, 129, 0.18);
            }
            .hero h1 { margin: 0 0 0.4rem 0; font-size: 2.1rem; }
            .hero p { margin: 0; opacity: 0.95; max-width: 760px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


PAGES = {
    "Home": render_home,
    "Upload Resume": render_upload_resume,
    "Upload Job Description": render_upload_job_description,
    "Skill Gap Analysis": render_skill_gap_analysis,
    "Learning Roadmap": render_learning_roadmap,
    "Mock Interview": render_mock_interview,
    "Evaluation Dashboard": render_evaluation_dashboard,
    "Interview History": render_interview_history,
    "Memory Dashboard": render_memory_dashboard,
    "Knowledge Base": render_knowledge_base,
    "Final Report": render_final_report,
}


def main() -> None:
    st.set_page_config(
        page_title="Multi-Agent RAG Interview Coach",
        page_icon="🧠",
        layout="wide",
    )

    _render_styles()

    st.markdown(
        "<div class='hero'><h1>Multi-Agent RAG Interview Coach</h1><p>Adaptive interview preparation with LangGraph orchestration, retrieval-augmented coaching, memory, and readiness tracking.</p></div>",
        unsafe_allow_html=True,
    )

    st.sidebar.title("Interview Coach Navigator")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    PAGES[selection]()


if __name__ == "__main__":
    main()
