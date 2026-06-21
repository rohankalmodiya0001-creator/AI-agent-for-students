import streamlit as st

from frontend.services.api_client import load_json


def render_evaluation_dashboard() -> None:
    st.header("Evaluation Dashboard")
    st.write("Track your technical, communication, problem solving, confidence, and readiness scores over time.")

    trends = load_json("performance_trends.json")
    if not trends:
        st.info("Complete a mock interview to generate evaluation results.")
        return

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Technical", f"{trends.get('technical_score', 0):.1f}")
    col2.metric("Communication", f"{trends.get('communication_score', 0):.1f}")
    col3.metric("Problem Solving", f"{trends.get('problem_solving_score', 0):.1f}")
    col4.metric("Confidence", f"{trends.get('confidence_score', 0):.1f}")
    col5.metric("Readiness", f"{trends.get('readiness_score', 0):.1f}")

    st.markdown("### Trend Snapshot")
    trend_table = {
        "Metric": ["Technical", "Communication", "Problem Solving", "Confidence", "Readiness"],
        "Score": [
            trends.get("technical_score", 0),
            trends.get("communication_score", 0),
            trends.get("problem_solving_score", 0),
            trends.get("confidence_score", 0),
            trends.get("readiness_score", 0),
        ],
    }
    st.bar_chart(trend_table, x="Metric", y="Score", use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown("### Weak Areas")
        weak_topics = trends.get("weak_topics", [])
        if weak_topics:
            for topic in weak_topics:
                st.write(f"- {topic}")
        else:
            st.write("- None recorded yet")
    with right:
        st.markdown("### Strong Areas")
        strong_topics = trends.get("strong_topics", [])
        if strong_topics:
            for topic in strong_topics:
                st.write(f"- {topic}")
        else:
            st.write("- None recorded yet")

    st.markdown("### Insight")
    if trends.get("readiness_score", 0) >= 80:
        st.success("You are in strong interview shape. Focus on consistency and polish.")
    elif trends.get("readiness_score", 0) >= 60:
        st.info("You are progressing well. Strengthen weak areas and repeat a mock interview.")
    else:
        st.warning("You need focused practice. Review the roadmap and rerun the adaptive interview loop.")
