import streamlit as st

from frontend.services.api_client import post


def render_memory_dashboard() -> None:
    st.header("Memory Dashboard")
    st.write("Review your session progress, weak topics, and interview history summaries.")

    session_id = st.text_input("Session ID", value="default")
    if st.button("Load session memory"):
        try:
            response = post(f"session/{session_id}/memory", {})
            st.markdown("<br><hr style='opacity: 0.15;'><br>", unsafe_allow_html=True)
            st.subheader("🧠 Active Session Memory")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total History Entries", response.get("history_length", 0))
            with col2:
                st.metric("Latest Questions Practiced", response.get("question_count", 0))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<div class="custom-card status-card-info">', unsafe_allow_html=True)
            st.markdown("#### 💬 Latest AI Coach Feedback")
            st.write(response.get("latest_feedback") or "*No feedback recorded yet. Complete mock interviews to start receiving coaching feedback.*")
            st.markdown('</div>', unsafe_allow_html=True)

            left, right = st.columns(2)
            with left:
                st.markdown('<div class="custom-card status-card-danger" style="height: 100%;">', unsafe_allow_html=True)
                st.markdown("#### 🔴 Weak Topics identified")
                weak_topics = response.get("weak_topics", [])
                if weak_topics:
                    pill_html = "".join([f'<span class="pill-badge pill-badge-red">{topic}</span>' for topic in weak_topics])
                    st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
                else:
                    st.write("*None recorded yet.*")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with right:
                st.markdown('<div class="custom-card status-card-success" style="height: 100%;">', unsafe_allow_html=True)
                st.markdown("#### 🟢 Strong Topics mastered")
                strong_topics = response.get("strong_topics", [])
                if strong_topics:
                    pill_html = "".join([f'<span class="pill-badge pill-badge-green">{topic}</span>' for topic in strong_topics])
                    st.markdown(f'<div style="margin-top:0.5rem;">{pill_html}</div>', unsafe_allow_html=True)
                else:
                    st.write("*None recorded yet.*")
                st.markdown('</div>', unsafe_allow_html=True)

            roadmap = response.get("adaptive_roadmap", [])
            if roadmap:
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("🎯 Active Study Roadmap Steps")
                st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
                for idx, step in enumerate(roadmap):
                    st.markdown(
                        f"""
                        <div class="timeline-item">
                            <div class="timeline-step">Step {idx + 1}</div>
                            <div class="custom-card" style="margin-top:0.25rem; margin-bottom:0; padding:1.2rem;">
                                {step}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("ℹ️ This dashboard reflects persistent interview memory stored by the backend.")
        except Exception as error:
            st.error(f"Failed to load session memory: {error}")
