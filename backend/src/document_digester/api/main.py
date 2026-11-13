import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from document_digester.api.routers.chat import router as chat_router
from document_digester.api.routers.search import router as search_router
from document_digester.service.generation import GenerationService
from document_digester.service.retrieval import RetrievalService
from document_digester.service.search import SearchService
from document_digester.service.ingestion.vectorization import (
    COLLECTION_NAME,
    create_vector_store
)
from document_digester.settings import settings


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Initializing Document Digester...")

    vector_store = create_vector_store()

    chunk_count = len(vector_store.get(include=[])["ids"])
    if chunk_count == 0:
        logger.warning(
            "The '%s' Chroma collection is empty. Index the docs with: "
            "uv run python -m document_digester.service.ingestion.index_docs",
            COLLECTION_NAME,
        )
    else:
        logger.info("Loaded %d chunks from '%s'.", chunk_count, COLLECTION_NAME)

    retrieval_service = RetrievalService(
        vector_store
    )

    app.state.search_service = SearchService(
        retrieval_service
    )

    app.state.generation_service = GenerationService(
        retrieval_service
    )

    logger.info(
        "Document Digester initialized (LLM: %s, embeddings: %s, Ollama: %s).",
        settings.LLM_MODEL,
        settings.EMBEDDING_MODEL,
        settings.OLLAMA_BASE_URL,
    )

    yield

    logger.info("Document Digester shutting down.")


app = FastAPI(
    title="Documentation Digester",
    description="Semantic search and RAG chat for Godot documentation",
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
app.include_router(chat_router)
