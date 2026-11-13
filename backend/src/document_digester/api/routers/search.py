import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.concurrency import run_in_threadpool

from document_digester.api.schemas import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from document_digester.service.search import SearchService


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)


def get_search_service(request: Request) -> SearchService:
    service = getattr(request.app.state, "search_service", None)

    if service is None:
        raise HTTPException(
            status_code=503,
            detail="Search service is not initialized."
        )

    return service


def format_search_result(result: dict) -> SearchResult:
    metadata = result.get("metadata", {})

    section_parts = [
        metadata.get("Header 2", ""),
        metadata.get("Header 3", "")
    ]

    section = " > ".join(
        part for part in section_parts if part
    )

    return SearchResult(
        content=result.get("text", ""),
        score=result.get("score"),
        source=metadata.get("title", "Godot Documentation"),
        section=section or metadata.get("title", ""),
        url=metadata.get("source")
    )


@router.post("/vector", response_model=SearchResponse)
async def vector_search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service)
):
    try:
        results = await run_in_threadpool(
            service.vector_search,
            request.query,
            request.top_k
        )

        return SearchResponse(
            query=request.query,
            results=[
                format_search_result(result)
                for result in results
            ]
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        logger.exception("Vector search failed.")

        raise HTTPException(
            status_code=500,
            detail="Vector search failed."
        )


@router.post("/hybrid", response_model=SearchResponse)
async def hybrid_search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service)
):
    try:
        results = await run_in_threadpool(
            service.hybrid_search,
            request.query,
            request.top_k
        )

        return SearchResponse(
            query=request.query,
            results=[
                format_search_result(result)
                for result in results
            ]
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        logger.exception("Hybrid search failed.")

        raise HTTPException(
            status_code=500,
            detail="Hybrid search failed."
        )
