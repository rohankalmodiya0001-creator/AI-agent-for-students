from pathlib import Path

import streamlit as st

from frontend.services.api_client import post, load_json


@st.cache_data(show_spinner=False)
def _fetch_documents() -> dict:
    return post("ingest/documents", {})


def render_knowledge_base() -> None:
    st.header("Knowledge Base Management")
    st.write("Ingest domain documents into the RAG knowledge base and explore stored knowledge sources.")

    if st.button("Ingest knowledge base"):
        try:
            response = post("ingest", {})
            st.success("Knowledge base ingestion completed.")
            st.json(response)
        except Exception as error:
            st.error(f"Knowledge base ingestion failed: {error}")

    if st.button("List available source documents"):
        try:
            documents = _fetch_documents()
            st.write("### Documents")
            st.json(documents)
        except Exception as error:
            st.error(f"Failed to list documents: {error}")

    if Path("src/data/raw_documents").exists():
        st.write("Source document directory:", str(Path("src/data/raw_documents")))
    else:
        st.info("Place text or markdown files under src/data/raw_documents to ingest them.")
