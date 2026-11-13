from typing import Literal

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=1000,
        description="The documentation search query."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of search results to return."
    )


class SearchResult(BaseModel):
    content: str = Field(
        description="The matching documentation content."
    )

    score: float | None = Field(
        default=None,
        description="The relevance score, if available."
    )

    source: str = Field(
        description="The source documentation."
    )

    section: str = Field(
        description="The documentation section."
    )

    url: str | None = Field(
        default=None,
        description="URL of the original documentation, if available."
    )


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]


class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=8000)


class ChatRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=1000,
        description="The user's question about the documentation."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of documentation chunks to give the LLM as context."
    )

    history: list[ChatTurn] = Field(
        default_factory=list,
        max_length=20,
        description="Previous turns in the conversation, oldest first."
    )


class ChatResponse(BaseModel):
    query: str
    answer: str
    sources: list[SearchResult]
