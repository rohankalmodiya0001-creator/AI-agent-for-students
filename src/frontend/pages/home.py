import streamlit as st


def render_home() -> None:
    st.subheader("Capstone-grade interview preparation workflow")
    cols = st.columns(4)
    cols[0].metric("Agents", "8", "specialized roles")
    cols[1].metric("Workflow", "LangGraph", "adaptive routing")
    cols[2].metric("Storage", "SQLite + Chroma", "memory + RAG")
    cols[3].metric("Interface", "Streamlit", "responsive multipage")

    st.markdown(
        """
        <div style='padding: 1.25rem 0; font-size: 1.05rem; line-height: 1.7;'>
            This platform helps technical candidates prepare for interviews using multi-agent orchestration,
            retrieval-augmented coaching, memory, evaluation, and adaptive preparation loops.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        st.markdown("### Core capabilities")
        st.markdown(
            "- Resume and job description parsing\n"
            "- Skill gap detection and readiness scoring\n"
            "- RAG-powered learning material retrieval\n"
            "- Adaptive interview question generation\n"
            "- Performance evaluation and trend tracking"
        )
    with right:
        st.markdown("### Workflow")
        st.markdown(
            "1. Upload resume\n"
            "2. Upload job description\n"
            "3. Run skill gap analysis\n"
            "4. Generate roadmap\n"
            "5. Take adaptive mock interview\n"
            "6. Review evaluation and final report"
        )
