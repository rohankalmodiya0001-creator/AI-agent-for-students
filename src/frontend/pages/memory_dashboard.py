import streamlit as st

from frontend.services.api_client import post


def render_memory_dashboard() -> None:
    st.header("Memory Dashboard")
    st.write("Review your session progress, weak topics, and interview history summaries.")

    session_id = st.text_input("Session ID", value="default")
    if st.button("Load session memory"):
        try:
            response = post(f"session/{session_id}/memory", {})
            st.subheader("Session Summary")
            col1, col2 = st.columns(2)
            col1.metric("History entries", response.get("history_length", 0))
            col2.metric("Latest questions", response.get("question_count", 0))

            st.write("### Latest feedback")
            st.write(response.get("latest_feedback") or "No feedback recorded yet.")

            left, right = st.columns(2)
            with left:
                st.write("### Weak topics")
                weak_topics = response.get("weak_topics", [])
                if weak_topics:
                    for topic in weak_topics:
                        st.write(f"- {topic}")
                else:
                    st.write("- None recorded yet")
            with right:
                st.write("### Strong topics")
                strong_topics = response.get("strong_topics", [])
                if strong_topics:
                    for topic in strong_topics:
                        st.write(f"- {topic}")
                else:
                    st.write("- None recorded yet")

            roadmap = response.get("adaptive_roadmap", [])
            if roadmap:
                st.write("### Adaptive roadmap")
                for step in roadmap:
                    st.write(f"- {step}")
            st.caption("This dashboard reflects persistent interview memory stored by the backend.")
        except Exception as error:
            st.error(f"Failed to load session memory: {error}")
