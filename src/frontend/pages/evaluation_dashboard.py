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
    col1.metric("Technical", f"{trends.get('technical_score', 0):.1f}%")
    col2.metric("Communication", f"{trends.get('communication_score', 0):.1f}%")
    col3.metric("Problem Solving", f"{trends.get('problem_solving_score', 0):.1f}%")
    col4.metric("Confidence", f"{trends.get('confidence_score', 0):.1f}%")
    col5.metric("Readiness", f"{trends.get('readiness_score', 0):.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📈 Performance Trend Snapshot")
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="custom-card status-card-danger" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("#### 🔴 Weak Areas to Focus")
        weak_topics = trends.get("weak_topics", [])
        if weak_topics:
            pill_html = "".join([f'<span class="pill-badge pill-badge-red">{topic}</span>' for topic in weak_topics])
            st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
        else:
            st.write("*None recorded yet. Keep it up!*")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with right:
        st.markdown('<div class="custom-card status-card-success" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("#### 🟢 Strong Areas Mastered")
        strong_topics = trends.get("strong_topics", [])
        if strong_topics:
            pill_html = "".join([f'<span class="pill-badge pill-badge-green">{topic}</span>' for topic in strong_topics])
            st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
        else:
            st.write("*None recorded yet. Complete mock interviews to discover strengths!*")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 AI Coach Insight")
    readiness = trends.get("readiness_score", 0)
    if readiness >= 80:
        st.markdown(
            f"""
            <div class="custom-card status-card-success" style="background: rgba(16, 185, 129, 0.08);">
                <h4 style="color:#10b981; margin:0;">🚀 High Readiness ({readiness:.1f}%)</h4>
                <p style="margin-top:0.5rem; margin-bottom:0; color:#cbd5e1;">
                    You are in strong interview shape! Focus on consistency, high-level system architecture, and polishing minor details.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif readiness >= 60:
        st.markdown(
            f"""
            <div class="custom-card status-card-info" style="background: rgba(59, 130, 246, 0.08);">
                <h4 style="color:#3b82f6; margin:0;">⚡ Good Progress ({readiness:.1f}%)</h4>
                <p style="margin-top:0.5rem; margin-bottom:0; color:#cbd5e1;">
                    You are progressing well. Strengthen the weak areas highlighted above, follow the custom study roadmap, and repeat the mock interview to boost your scores.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="custom-card status-card-warning" style="background: rgba(245, 158, 11, 0.08);">
                <h4 style="color:#f59e0b; margin:0;">⚠️ Needs Focused Practice ({readiness:.1f}%)</h4>
                <p style="margin-top:0.5rem; margin-bottom:0; color:#cbd5e1;">
                    You need focused practice. Spend extra time reviewing your personalized learning roadmap, study key concepts, and run the adaptive mock interview loop again.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

