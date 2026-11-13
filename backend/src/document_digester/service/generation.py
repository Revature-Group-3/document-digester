import logging
from time import perf_counter

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from document_digester.settings import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Document Digester, an assistant that answers questions \
about the Godot game engine using ONLY the documentation excerpts provided.

Rules:
- Base your answer strictly on the context below. If the context does not contain \
the answer, say you could not find it in the documentation.
- Cite the excerpts you used with their bracketed numbers, e.g. [1] or [2][3].
- Keep answers concise and include short code examples when the context has them.

Context:
{context}"""

NO_CONTEXT_ANSWER = (
    "I couldn't find anything relevant in the indexed documentation. "
    "Make sure the docs have been indexed (see backend/README.md)."
)


def create_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
    )


def format_context(results: list[dict]) -> str:
    blocks = []
    for number, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})
        heading = " > ".join(
            part
            for part in (
                metadata.get("title", ""),
                metadata.get("Header 2", ""),
                metadata.get("Header 3", ""),
            )
            if part
        )
        blocks.append(f"[{number}] {heading}\n{result.get('text', '')}")
    return "\n\n".join(blocks)


class GenerationService:
    """Retrieval-augmented generation: retrieve chunks, then ask the local LLM."""

    def __init__(self, retrieval_service, llm: BaseChatModel | None = None):
        self.retrieval_service = retrieval_service
        self.llm = llm or create_llm()

    def answer(
        self,
        query: str,
        top_k: int = 5,
        history: list[dict] | None = None,
    ) -> dict:
        results = self.retrieval_service.retrieve_hybrid(query, k=top_k)

        if not results:
            return {"answer": NO_CONTEXT_ANSWER, "sources": []}

        messages: list[BaseMessage] = [
            SystemMessage(SYSTEM_PROMPT.format(context=format_context(results)))
        ]
        for turn in history or []:
            content = turn.get("content", "")
            if not content:
                continue
            if turn.get("role") == "assistant":
                messages.append(AIMessage(content))
            else:
                messages.append(HumanMessage(content))
        messages.append(HumanMessage(query))

        start = perf_counter()
        response = self.llm.invoke(messages)
        logger.info("LLM generation latency: %.2f ms", (perf_counter() - start) * 1000)

        return {"answer": str(response.content).strip(), "sources": results}
