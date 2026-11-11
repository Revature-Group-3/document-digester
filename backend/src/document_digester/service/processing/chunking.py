from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from document_digester.settings import EMBEDDING_MODEL
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

def chunk_page(html : str, metadata: dict) :
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
    characterSplitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap=200
    )

    #4.
    chunks = splitter.split_documents(sections)
    chunks = characterSplitter.split_documents(chunks)

    for index, chunk in enumerate(chunks):
        chunk.metadata.update({
            "title": metadata["title"],
            "source": metadata["source"],
            "chunk_idex": index,
        })

    return chunks