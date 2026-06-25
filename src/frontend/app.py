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
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

            /* Typography */
            html, body, [class*="css"], .stApp {
                font-family: 'Plus Jakarta Sans', sans-serif;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 600;
            }

            /* Base modifications */
            .block-container { 
                padding-top: 1.5rem; 
                padding-bottom: 1.5rem;
            }

            /* Custom Hero Section */
            .hero {
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 50%, #312e81 100%);
                color: #FFFFFF;
                border-radius: 18px;
                padding: 2rem 2.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                position: relative;
                overflow: hidden;
            }
            .hero::after {
                content: '';
                position: absolute;
                top: -50%;
                right: -20%;
                width: 300px;
                height: 300px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 50%;
                pointer-events: none;
            }
            .hero h1 { 
                margin: 0 0 0.5rem 0; 
                font-size: 2.3rem; 
                letter-spacing: -0.02em;
            }
            .hero p { 
                margin: 0; 
                opacity: 0.9; 
                font-size: 1.05rem;
                max-width: 800px; 
            }

            /* Glass Cards */
            .custom-card {
                background: rgba(19, 28, 49, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .custom-card:hover {
                transform: translateY(-2px);
                border-color: rgba(99, 102, 241, 0.3);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
                background: rgba(19, 28, 49, 0.6);
            }

            /* Status Cards */
            .status-card-success {
                border-left: 4px solid #10b981;
            }
            .status-card-warning {
                border-left: 4px solid #f59e0b;
            }
            .status-card-danger {
                border-left: 4px solid #ef4444;
            }
            .status-card-info {
                border-left: 4px solid #3b82f6;
            }

            /* Pill Badges */
            .pill-badge {
                display: inline-flex;
                align-items: center;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 550;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
                background: rgba(99, 102, 241, 0.15);
                color: #a5b4fc;
                border: 1px solid rgba(99, 102, 241, 0.3);
                transition: all 0.2s ease;
                cursor: default;
            }
            .pill-badge:hover {
                background: rgba(99, 102, 241, 0.25);
                transform: scale(1.05);
            }
            .pill-badge-green {
                background: rgba(16, 185, 129, 0.15);
                color: #6ee7b7;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            .pill-badge-red {
                background: rgba(239, 68, 68, 0.15);
                color: #fca5a5;
                border: 1px solid rgba(239, 68, 68, 0.3);
            }
            .pill-badge-yellow {
                background: rgba(245, 158, 11, 0.15);
                color: #fde047;
                border: 1px solid rgba(245, 158, 11, 0.3);
            }

            /* Timeline */
            .timeline-item {
                border-left: 2px solid rgba(99, 102, 241, 0.3);
                padding-left: 1.5rem;
                position: relative;
                padding-bottom: 1.5rem;
            }
            .timeline-item::before {
                content: '';
                position: absolute;
                left: -6px;
                top: 4px;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #6366f1;
                border: 2px solid #0b0f19;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
            }
            .timeline-step {
                font-weight: 700;
                font-size: 1.1rem;
                color: #a5b4fc;
                margin-bottom: 0.25rem;
            }

            /* Custom interactive overrides */
            div.stButton > button {
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
                color: white !important;
                border: none !important;
                padding: 0.6rem 2rem !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            div.stButton > button:hover {
                background: linear-gradient(135deg, #4f46e5 0%, #3b37c3 100%) !important;
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
                transform: translateY(-2px) !important;
                border-color: transparent !important;
            }
            div.stButton > button:active {
                transform: translateY(0) !important;
            }

            /* Sidebar Styling */
            section[data-testid="stSidebar"] {
                background-color: #0b0f19 !important;
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }
            section[data-testid="stSidebar"] .stRadio > div {
                gap: 5px;
            }

            /* Metric styling */
            div[data-testid="stMetric"] {
                background: rgba(19, 28, 49, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 0.8rem 1.2rem;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            div[data-testid="stMetricValue"] {
                font-weight: 700;
                color: #6366f1;
            }
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
