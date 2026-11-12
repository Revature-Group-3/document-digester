import logging

from fastapi import FastAPI, HTTPException
from document_digester.models import SearchRequest, SearchResponse
from document_digester.service.search import search_documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Documentation Digester",
    description="Semantic search for Godot documentation",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Documentation Digester API"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/api/search",
    response_model=SearchResponse,
    summary="Search documentation",
    description="Search Godot documentation and return ranked results with source information."
)
def search(request: SearchRequest):

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty"
        )

    try:
        logger.info("Searching documentation: %s", request.query)

        results = search_documents(
            request.query,
            request.top_k
        )

        return SearchResponse(
            query=request.query,
            results=results
        )

    except Exception:
        logger.exception("An error occurred during document retrieval")

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while searching documents"
        )
