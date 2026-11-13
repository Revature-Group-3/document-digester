# Evaluation

Measures how well search finds the right doc section for a set of real-style questions.
The scope is the 7 pages in `docs/`.

- `golden_set.jsonl`: 39 questions, each labeled with the page and section that answers it (`also_relevant` lists other sections that also count).
- `evaluation/metrics.py`: hit@k, MRR, precision@k.
- `evaluation/baseline.py`: simple retriever over the same `docs/` pages (split by heading, no cleaning or vector DB). This is the floor to beat.
- `evaluation/run_eval.py`: runs the questions through our `RetrievalService` and reports accuracy, latency and provenance for semantic and hybrid search.

## Run against our pipeline

Needs Ollama running with `all-minilm` and the Chroma index built (see `backend/README.md`).

```bash
cd backend
uv run python -m document_digester.evaluation.run_eval
```

## Run the baseline

```bash
cd backend
uv run --with sentence-transformers python -m document_digester.evaluation.baseline
```
