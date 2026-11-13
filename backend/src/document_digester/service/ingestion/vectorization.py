from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from document_digester.settings import settings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

COLLECTION_NAME = "godot_docs"


def create_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )


def create_vector_store() -> Chroma:
    persist_directory = Path(settings.CHROMA_PERSIST_DIRECTORY)
    persist_directory.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=create_embeddings(),
        persist_directory=str(persist_directory),
    )


def embed_and_store_chunks(chunks: list[Document], vector_store: Chroma) -> int:
    if not chunks:
        raise ValueError("No chunks were provided for vectorization.")

    source_urls: set[str] = set()
    ids: list[str] = []
    for chunk in chunks:
        source = chunk.metadata.get("source")
        chunk_index = chunk.metadata.get("chunk_index")
        if not isinstance(source, str) or not source:
            raise ValueError("Every chunk must have a non-empty source URL.")
        if not isinstance(chunk_index, int):
            raise ValueError("Every chunk must have an integer chunk_index.")

        source_urls.add(source)
        chunk.metadata.setdefault("Header 2", "")
        chunk.metadata.setdefault("Header 3", "")
        ids.append(str(uuid5(NAMESPACE_URL, f"{source}#chunk-{chunk_index}")))

    if len(set(ids)) != len(ids):
        raise ValueError("Chunks must have unique source URL and chunk_index pairs.")

    existing = vector_store.get(
        where={"source": {"$in": sorted(source_urls)}},
        include=["metadatas"],
    )
    existing_ids = set(existing["ids"])

    vector_store.add_documents(chunks, ids=ids)

    stale_ids = existing_ids - set(ids)
    if stale_ids:
        vector_store.delete(ids=sorted(stale_ids))

    return len(chunks)
