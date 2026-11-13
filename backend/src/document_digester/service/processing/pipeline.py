from document_digester.service.ingestion.loader import load_pages
from document_digester.service.processing.cleaning import clean_html
from document_digester.service.processing.chunking import chunk_page


def run_pipeline():
    chunked_list = []
    for page in load_pages():
        cleaned = clean_html(page["body"])
        # then chunk it
        chunked = chunk_page(cleaned, {"title": page["title"], "source": page["source"]})

        # Since chunk_page returns a list of chunks, extend gives you one flat list of all the chunks. basically we are "flattening it out"
        chunked_list.extend(chunked)
    return chunked_list

if __name__=="__main__":
    chunks = run_pipeline()
    print(len(chunks))
    print(chunks[5])
    print(max(len(c.page_content) for c in chunks))           # should be ≤ 1000
    print(sum(1 for c in chunks if len(c.page_content) < 200)) # tiny ones, should be about 0