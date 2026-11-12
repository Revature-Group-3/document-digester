from document_digester.service.ingestion.vectorization import (
    create_vector_store,
    embed_and_store_chunks,
)
from document_digester.service.processing import chunking
from document_digester.settings import settings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


class TestEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(text)), float(sum(map(ord, text)) % 997)] for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return [float(len(text)), float(sum(map(ord, text)) % 997)]


def test_embed_store_and_replace_chunks_for_source(tmp_path) -> None:
    vector_store = Chroma(
        collection_name="test_godot_docs",
        embedding_function=TestEmbeddings(),
        persist_directory=str(tmp_path),
    )
    original_chunks = [
        Document(
            page_content="Original first section",
            metadata={
                "source": "https://docs.example/page",
                "title": "Page",
                "chunk_index": 0,
                "Header 2": "First section",
                "Header 3": "",
            },
        ),
        Document(
            page_content="Original second section",
            metadata={
                "source": "https://docs.example/page",
                "title": "Page",
                "chunk_index": 1,
                "Header 2": "Second section",
                "Header 3": "Nested section",
            },
        ),
    ]

    assert embed_and_store_chunks(original_chunks, vector_store) == 2
    assert len(vector_store.get(include=["metadatas"])["ids"]) == 2

    updated_chunks = [
        Document(
            page_content="Updated first section",
            metadata={
                "source": "https://docs.example/page",
                "title": "Page",
                "chunk_index": 0,
                "Header 2": "First section",
                "Header 3": "",
            },
        ),
    ]
    assert embed_and_store_chunks(updated_chunks, vector_store) == 1

    stored = vector_store.get(include=["documents", "metadatas"])
    assert stored["documents"] == ["Updated first section"]
    assert stored["metadatas"] == [
        {
            "source": "https://docs.example/page",
            "title": "Page",
            "chunk_index": 0,
            "Header 2": "First section",
            "Header 3": "",
        }
    ]


def test_create_vector_store_uses_configured_persistent_directory(
    tmp_path, monkeypatch
) -> None:
    persist_directory = tmp_path / "chroma"
    monkeypatch.setattr(
        settings,
        "CHROMA_PERSIST_DIRECTORY",
        str(persist_directory),
    )

    vector_store = create_vector_store()

    assert persist_directory.is_dir()
    assert vector_store.get(include=["metadatas"])["ids"] == []


def test_chunk_page_keeps_source_and_both_heading_levels(monkeypatch) -> None:
    monkeypatch.setattr(chunking, "embeddings", TestEmbeddings())

    text = (
        "## Main section\n"
        "### Nested section\n"
        + ("This paragraph describes a Godot feature in enough detail. " * 20)
    )
    chunks = chunking.chunk_page(
        text,
        {"title": "Godot guide", "source": "https://docs.example/page"},
    )

    assert chunks
    assert all(chunk.metadata["source"] == "https://docs.example/page" for chunk in chunks)
    assert all(chunk.metadata["Header 2"] == "Main section" for chunk in chunks)
    assert all(chunk.metadata["Header 3"] == "Nested section" for chunk in chunks)
    assert all("title" in chunk.metadata for chunk in chunks)
