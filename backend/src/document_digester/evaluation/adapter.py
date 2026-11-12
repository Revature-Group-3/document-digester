"""Turn the pipeline's chunk metadata into the (page, section) labels the question set uses."""

import re

DOCS_URL = re.compile(r"^https?://docs\.godotengine\.org/[^/]+/[^/]+/(?P<page>.+?)\.html")


def page_from_url(url):
    """https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html
    -> getting_started/step_by_step/signals
    """
    match = DOCS_URL.match(url or "")
    return match.group("page") if match else None


def normalize(text):
    """Headings differ slightly between raw .rst and Sphinx text output (backticks, escapes)."""
    return re.sub(r"\s+", " ", re.sub(r"[`\\*]", "", text or "")).strip().lower()


def chunk_labels(metadata):
    """All (page, section) labels a chunk belongs to, most specific first.

    A chunk under "### Custom signals" inside "## Using signals" belongs to both.
    Chunks before the first heading fall back to the page title.
    """
    page = page_from_url(metadata.get("source"))
    if not page:
        return []
    headings = [metadata.get("Header 3"), metadata.get("Header 2"), metadata.get("title")]
    return [(page, normalize(h)) for h in headings if h]


def normalize_question(question):
    """Copy of a question with its labels normalized the same way as chunk labels."""
    q = dict(question)
    q["section"] = normalize(q["section"])
    q["also_relevant"] = [[page, normalize(section)] for page, section in q.get("also_relevant", [])]
    return q
