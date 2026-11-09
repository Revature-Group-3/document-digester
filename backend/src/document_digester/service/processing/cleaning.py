from bs4 import BeautifulSoup

# returns cleaned html
def clean_html(html : str ) -> str:
    pages = BeautifulSoup(html, "html.parser")
    # 1. purge scripts and styles
    for tag in pages(["script", "style"]):
        tag.decompose()

    for tag in pages.select("a.headerlink"):
        tag.decompose()

    for tag in pages.find_all("img"):
        tag.decompose()

    return str(pages)
