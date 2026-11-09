from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    sections = html_header_splitter.split_text(html)

    splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,

            )
    
    chunks = splitter.split_documents(sections)

    for index, chunk in enumerate(chunks):
        chunk.metadata.update({
            "title": metadata["title"],
            "source": metadata["source"],
            "chunk_idex": index,
        })

    return chunks