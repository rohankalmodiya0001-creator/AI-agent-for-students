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
    for idx, item in enumerate(questions):
        st.subheader(f"Question {idx + 1}")
        st.write(item["question"])
        answer = st.text_area(f"Answer {idx + 1}", key=f"answer_{idx}", height=150)
        answers.append(answer)

    if st.button("Submit interview answers"):
        try:
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
            st.success("Interview answers evaluated successfully.")
            st.json(response["performance_trends"])
        except Exception as error:
            st.error(f"Failed to evaluate answers: {error}")
