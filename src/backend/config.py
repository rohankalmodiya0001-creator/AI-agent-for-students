from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    google_project_id: str = Field(default="", alias="GOOGLE_PROJECT_ID")
    database_url: str = Field(default="sqlite:///./src/data/app.db", alias="DATABASE_URL")
    chroma_db_dir: str = Field(default="./src/data/embeddings", alias="CHROMA_DB_DIR")
    docs_path: str = Field(default="./src/data/raw_documents", alias="DOCS_PATH")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    streamlit_server_port: int = Field(default=8501, alias="STREAMLIT_SERVER_PORT")


config = AppConfig()
