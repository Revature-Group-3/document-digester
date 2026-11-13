import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from ollama import ResponseError
from starlette.concurrency import run_in_threadpool

from document_digester.api.routers.search import format_search_result
from document_digester.api.schemas import ChatRequest, ChatResponse
from document_digester.service.generation import GenerationService
from document_digester.settings import settings


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


def get_generation_service(request: Request) -> GenerationService:
    service = getattr(request.app.state, "generation_service", None)

    if service is None:
        raise HTTPException(
            status_code=503,
            detail="Generation service is not initialized."
        )

    return service


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: GenerationService = Depends(get_generation_service)
):
    try:
        result = await run_in_threadpool(
            service.answer,
            request.query,
            request.top_k,
            [turn.model_dump() for turn in request.history],
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except (httpx.ConnectError, ConnectionError):
        logger.exception("Could not reach Ollama.")
        raise HTTPException(
            status_code=503,
            detail=(
                f"Could not reach Ollama at {settings.OLLAMA_BASE_URL}. "
                "Is `ollama serve` running?"
            ),
        )

    except ResponseError as error:
        # e.g. "model not found" — surface it so the user knows to `ollama pull`.
        logger.exception("Ollama returned an error.")
        raise HTTPException(status_code=502, detail=f"Ollama error: {error.error}")

    except Exception:
        logger.exception("Chat generation failed.")
        raise HTTPException(status_code=500, detail="Chat generation failed.")

    return ChatResponse(
        query=request.query,
        answer=result["answer"],
        sources=[format_search_result(source) for source in result["sources"]],
    )
