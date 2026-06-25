FROM python:3.14-slim

WORKDIR /app

COPY requirements-full.txt ./
RUN pip install --no-cache-dir -r requirements-full.txt

# Copy only source + required small assets.
# Large persistent runtime data (Chroma/embeddings, sqlite, etc.) should be mounted at runtime.
# Keep Docker build context small by copying only the required folders.
COPY pyproject.toml ./
COPY requirements.txt ./
COPY src ./src
COPY docs ./docs
COPY tests ./tests
COPY README.md ./README.md
COPY ARCHITECTURE.md ./ARCHITECTURE.md
COPY .env.example ./

ENV PYTHONPATH=/app/src
ENV STREAMLIT_SERVER_PORT=8501


EXPOSE 8000 8501

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
