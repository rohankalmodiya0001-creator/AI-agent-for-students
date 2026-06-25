from pathlib import Path

import streamlit as st

from frontend.services.api_client import load_json, post, save_json


def render_final_report() -> None:
    st.header("Final Interview Readiness Report")
    st.write("The final report summarizes strengths, weaknesses, readiness, and next actions.")

    final_report_path = Path("src/data/final_report.txt")
    skill_gap_report = load_json("skill_gap_report.json")
    performance_trends = load_json("performance_trends.json")

    if final_report_path.exists():
        report_text = final_report_path.read_text(encoding="utf-8")
        st.markdown('<div class="custom-card status-card-success">', unsafe_allow_html=True)
        st.markdown("#### ✅ Saved Report Exists")
        st.write("Your final readiness report has been compiled and is ready for download.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.text_area("Readiness Report Contents", value=report_text, height=450)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "📥 Download Final Report (.txt)",
            report_text,
            file_name="final_report.txt",
            mime="text/plain",
        )
        return

    if not skill_gap_report or not performance_trends:
        st.info("Complete evaluation first to generate the final report.")
        return

    if st.button("Generate final report"):
        try:
            with st.spinner("Generating final readiness report..."):
                response = post(
                    "final-report",
                    {
                        "skill_gap_report": skill_gap_report,
                        "performance_trends": performance_trends,
                    },
                )
                report_text = response["final_report"]
                final_report_path.write_text(report_text, encoding="utf-8")
                st.success("Final report generated successfully.")
                st.text_area("Readiness Report Contents", value=report_text, height=450)
                st.download_button(
                    "📥 Download Final Report (.txt)",
                    report_text,
                    file_name="final_report.txt",
                    mime="text/plain",
                )
        except Exception as error:
            st.error(f"Failed to generate final report: {error}")

