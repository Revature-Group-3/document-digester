from document_digester.service.ingestion.vectorization import (
    COLLECTION_NAME,
    create_vector_store,
    embed_and_store_chunks,
)
from document_digester.service.processing.pipeline import run_pipeline


def main() -> None:
    chunks = run_pipeline()
    vector_store = create_vector_store()
    count = embed_and_store_chunks(chunks, vector_store)
    print(f"Indexed {count} chunks in the '{COLLECTION_NAME}' collection.")


if __name__ == "__main__":
    main()
