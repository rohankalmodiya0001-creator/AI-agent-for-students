import streamlit as st

from frontend.services.api_client import load_json


def render_interview_history() -> None:
    st.header("Interview History")
    st.write("See prior mock interview questions, answers, and feedback.")

    history = load_json("interview_history.json")
    if not history:
        st.info("No interview history available yet.")
        return

    for record in history:
        st.subheader(record.get("question", "Question"))
        st.write(f"**Answer:** {record.get('answer', '')}")
        st.write(f"**Feedback:** {record.get('feedback', '')}")
        st.write(f"**Topic:** {record.get('topic', '')}")
        st.write("---")
