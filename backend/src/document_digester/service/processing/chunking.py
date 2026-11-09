from langchain_text_splitters import HTMLHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_page(html : str, metadata: dict) :
    header_to_split_on=[
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3")
        ]

    html_header_splitter = HTMLHeaderTextSplitter(
            headers_to_split_on=header_to_split_on,
            )
    sections = html_header_splitter.split_text(html)


    # split document by relevant tags
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