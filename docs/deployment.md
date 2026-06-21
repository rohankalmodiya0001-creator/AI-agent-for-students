# Deployment Guide

This project supports three deployment paths:
- Local development for full backend + Streamlit usage
- Docker Compose for containerized local or server deployment
- Streamlit Cloud for the frontend demo experience

## Prerequisites

- Python 3.11 or newer
- A Google Gemini API key
- Git
- Docker and Docker Compose, if you want container deployment

## Environment Variables

Create a `.env` file from `.env.example` and set these values:

- `GOOGLE_API_KEY`
- `GOOGLE_PROJECT_ID`
- `DATABASE_URL` if you want to override the default SQLite path
- `CHROMA_DB_DIR` if you want a custom vector store directory
- `DOCS_PATH` if you want a different knowledge-base folder
- `LOG_LEVEL`

The defaults store application data under `src/data`.

## Local Deployment

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and set your API key values.
5. Start the backend API:

   ```powershell
   python src/backend/run.py
   ```

6. Start the Streamlit frontend in a second terminal:

   ```powershell
   python src/frontend/run.py
   ```

7. Open the app at `http://localhost:8501`.

Backend API defaults:
- Host: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- API prefix: `http://localhost:8000/api`

## Docker Compose Deployment

Docker Compose is the easiest way to run both services together.

1. Make sure `.env` exists in the project root.
2. Build and start the containers:

   ```powershell
   docker compose up --build
   ```

3. Open the frontend at `http://localhost:8501`.
4. The backend will be available at `http://localhost:8000`.

The compose file mounts `src/data` into the containers so the SQLite database and ChromaDB vectors persist across restarts.

## Streamlit Cloud Deployment

Use Streamlit Cloud when you want to host the frontend demo.

1. Push the repository to GitHub.
2. In Streamlit Cloud, create a new app from the repository.
3. Set the app entry point to `src/frontend/app.py`.
4. Add the following secrets or environment variables:
   - `GOOGLE_API_KEY`
   - `GOOGLE_PROJECT_ID`
   - `API_BASE_URL` if the backend is hosted separately
5. Deploy the app.

If the backend is not deployed alongside Streamlit Cloud, point `API_BASE_URL` to the hosted backend before using the app.

## Production Notes

- Keep `src/data/raw_documents` populated with domain content for RAG ingestion.
- SQLite is fine for local and demo use, but PostgreSQL is a better long-term option for production.
- ChromaDB embeddings live in `src/data/embeddings` by default.
- The knowledge base should be ingested before running the adaptive interview loop for the best results.

## Troubleshooting

- If the frontend cannot reach the backend, check `API_BASE_URL` and confirm the backend is running on port `8000`.
- If RAG retrieval is empty, confirm `src/data/raw_documents` contains `.txt` or `.md` files and run the knowledge-base ingestion step.
- If the app cannot find your `.env`, verify that it is located at the project root.
