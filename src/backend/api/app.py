from contextlib import asynccontextmanager

from fastapi import FastAPI

from ..database import initialize_database
from ..app_logging import logger
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    logger.info("Starting Multi-Agent RAG Interview Coach API")
    try:
        yield
    finally:
        logger.info("Shutting down API")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Multi-Agent RAG Interview Coach API",
        description="API endpoints powering the interview coaching agent system.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(router, prefix="/api")

    # Root-level health endpoint for quick checks (tests expect `/health`).
    @app.get("/health")
    def root_health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
