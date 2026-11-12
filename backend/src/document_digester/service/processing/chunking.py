from document_digester.settings import settings
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

embeddings = OllamaEmbeddings(model=settings.EMBEDDING_MODEL)

def chunk_page(html: str, metadata: dict[str, str]) -> list[Document]:
    header_to_split_on=[
            ("##", "Header 2"),
            ("###", "Header 3")
        ]

    # strip_header=False so header stays inside chunk
    html_header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=header_to_split_on,
            strip_headers=False
            )

    # 1.
    sections = html_header_splitter.split_text(html)

    #2.
    splitter = SemanticChunker(
        embeddings,
        min_chunk_size=200
        )
    #3.
    character_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )

    #4.
    chunks = splitter.split_documents(sections)
    chunks = character_splitter.split_documents(chunks)

    for index, chunk in enumerate(chunks):
        chunk.metadata.update({
            "title": metadata["title"],
            "source": metadata["source"],
            "chunk_index": index,
        })
        chunk.metadata.setdefault("Header 2", "")
        chunk.metadata.setdefault("Header 3", "")

    return chunks