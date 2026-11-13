import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from document_digester.api.routers.search import router as search_router
from document_digester.service.retrieval import RetrievalService
from document_digester.service.search import SearchService
from document_digester.service.ingestion.vectorization import (
    create_vector_store
)


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Initializing Document Digester...")

    vector_store = create_vector_store()

    retrieval_service = RetrievalService(
        vector_store
    )

    app.state.search_service = SearchService(
        retrieval_service
    )

    logger.info("Document Digester initialized.")

    yield

    logger.info("Document Digester shutting down.")


app = FastAPI(
    title="Documentation Digester",
    description="Semantic search for Godot documentation",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {
        "message": "Documentation Digester API"
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy"
    }


app.include_router(search_router)
