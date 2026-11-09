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
    print(len(run_pipeline()))