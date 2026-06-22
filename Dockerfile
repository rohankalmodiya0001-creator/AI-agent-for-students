FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only source + required small assets.
# Large persistent runtime data (Chroma/embeddings, sqlite, etc.) should be mounted at runtime.
COPY . .


ENV PYTHONPATH=/app/src
ENV STREAMLIT_SERVER_PORT=8501

EXPOSE 8000 8501

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
