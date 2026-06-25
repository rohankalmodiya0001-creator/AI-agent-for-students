import json
from pathlib import Path

import streamlit as st

from frontend.services.api_client import load_json, post, save_json


def render_mock_interview() -> None:
    st.header("Mock Interview")
    st.write("Answer the adaptive interview questions generated from your skill gap analysis.")

    skill_gap_report = load_json("skill_gap_report.json")
    questions_path = Path("src/data/interview_questions.json")
    interview_type = st.selectbox(
        "Interview type",
        [
            "Machine Learning",
            "Data Science",
            "Deep Learning",
            "LLM",
            "RAG",
            "MLOps",
            "Python",
            "System Design",
        ],
    )

    if not skill_gap_report:
        st.warning("Run skill gap analysis before generating interview questions.")
        return

    if st.button("Generate interview questions"):
        try:
            response = post("mock-interview", {"skill_gap_report": skill_gap_report, "interview_type": interview_type})
            save_json("interview_questions.json", response["questions"])
            st.success("Interview questions generated successfully.")
            st.rerun()
        except Exception as error:
            st.error(f"Failed to generate questions: {error}")
            return

    if not questions_path.exists():
        st.info("Press 'Generate interview questions' to start the mock interview.")
        return

    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    answers = []
    
    st.markdown("<br><hr style='opacity: 0.15;'><br>", unsafe_allow_html=True)
    st.subheader("📝 Live Mock Interview Q&A")
    
    for idx, item in enumerate(questions):
        topic = item.get("topic", "General")
        diff = item.get("difficulty", "Medium")
        
        diff_class = "pill-badge-yellow"
        if diff.lower() == "easy":
            diff_class = "pill-badge-green"
        elif diff.lower() == "hard":
            diff_class = "pill-badge-red"
            
        st.markdown(
            f"""
            <div class="custom-card" style="margin-bottom: 0.5rem; border-left: 4px solid #6366f1; padding: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 0.5rem;">
                    <strong style="color: #6366f1; font-size: 1.1rem;">Question {idx + 1}</strong>
                    <div>
                        <span class="pill-badge" style="margin-bottom:0;">{topic}</span>
                        <span class="pill-badge {diff_class}" style="margin-bottom:0;">{diff}</span>
                    </div>
                </div>
                <div style="font-size: 1.05rem; line-height: 1.5; color: #f8fafc;">
                    {item["question"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        answer = st.text_area("Your response:", key=f"answer_{idx}", height=120, placeholder="Type your detailed technical answer here...", label_visibility="collapsed")
        answers.append(answer)
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Submit interview answers"):
        try:
            with st.spinner("Evaluating your responses..."):
                response = post(
                    "evaluate",
                    {
                        "session_id": "default",
                        "questions": questions,
                        "answers": answers,
                    },
                )
                save_json("interview_history.json", response["interview_history"])
                save_json("performance_trends.json", response["performance_trends"])
                save_json("interview_answers.json", answers)
                st.success("Interview answers evaluated successfully! Go to the Evaluation Dashboard to see your scores.")
        except Exception as error:
            st.error(f"Failed to evaluate answers: {error}")

