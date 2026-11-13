from document_digester.evaluation.adapter import chunk_labels, normalize_question, page_from_url
from document_digester.evaluation.run_eval import answerable, run_mode

SIGNALS_URL = "https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html"


def chunk(header2="", header3="", source=SIGNALS_URL, title="Using signals"):
    return {"metadata": {"source": source, "title": title, "Header 2": header2, "Header 3": header3}}


def test_page_from_url():
    assert page_from_url(SIGNALS_URL) == "getting_started/step_by_step/signals"
    assert page_from_url("https://docs.godotengine.org/en/latest/classes/class_timer.html") == "classes/class_timer"
    assert page_from_url("not a url") is None
    assert page_from_url(None) is None


def test_chunk_labels_most_specific_first():
    labels = chunk_labels(chunk("Custom signals", "Declaring")["metadata"])
    page = "getting_started/step_by_step/signals"
    assert labels == [(page, "declaring"), (page, "custom signals"), (page, "using signals")]


def test_intro_chunk_falls_back_to_title():
    assert chunk_labels(chunk()["metadata"]) == [("getting_started/step_by_step/signals", "using signals")]


def test_normalize_question_strips_rst_markup():
    q = normalize_question({"page": "p", "section": "Accessing ``user://``", "also_relevant": [["p", "Base *size*"]]})
    assert q["section"] == "accessing user://"
    assert q["also_relevant"] == [["p", "base size"]]


def test_run_mode_scores_retriever_output():
    golden = [normalize_question({
        "id": "q1", "type": "direct", "question": "connect in code?",
        "page": "getting_started/step_by_step/signals", "section": "Connecting a signal via code",
    })]

    def search(query, k):
        print("Retrieval Latency: 1 ms")  # real retriever prints; run_mode should swallow it
        return [chunk("Scene setup"), chunk("Connecting a signal via code")][:k]

    summary = run_mode(search, golden, k=5)

    assert summary["all"]["hit@5"] == 1.0
    assert summary["all"]["mrr"] == 0.5
    assert summary["provenance"] == 1.0
    assert summary["latency_ms"]["p50"] >= 0


def test_missing_metadata_counts_against_provenance():
    golden = [normalize_question({"id": "q1", "type": "direct", "question": "?", "page": "a", "section": "b"})]
    summary = run_mode(lambda q, k: [{"metadata": {"title": "No source"}}], golden, k=5)
    assert summary["provenance"] == 0.0


def test_answerable_only_keeps_questions_whose_page_is_indexed():
    golden = [
        {"id": "q1", "page": "a", "section": "x"},
        {"id": "q2", "page": "b", "section": "y", "also_relevant": [["a", "z"]]},
        {"id": "q3", "page": "c", "section": "w"},
    ]
    assert [q["id"] for q in answerable(golden, {"a"})] == ["q1", "q2"]


def test_baseline_splits_sphinx_text_pages(tmp_path):
    from document_digester.evaluation.baseline import split_sections

    page = tmp_path / "signals.txt"
    page.write_text(
        "Using signals\n"
        f"{SIGNALS_URL}\n"
        "*************\n"
        "Intro text.\n"
        "\n"
        "Connecting a signal via code\n"
        "============================\n"
        "Call connect().\n"
        "\n"
        "Declaring\n"
        "---------\n"
        "Use the signal keyword.\n",
        encoding="utf-8",
    )

    sections = [(p, s) for p, s, _ in split_sections(page)]
    page_name = "getting_started/step_by_step/signals"
    assert sections == [
        (page_name, "using signals"),
        (page_name, "connecting a signal via code"),
        (page_name, "declaring"),
    ]
