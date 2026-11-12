# Evaluation

Measures how well search finds the right doc section for a set of real-style questions.

- `golden_set.jsonl`: 50 questions, each labeled with the page and section that answers it (`also_relevant` lists other sections that also count).
- `evaluation/metrics.py`: hit@k, MRR, precision@k.
- `evaluation/baseline.py`: simple standalone retriever (raw .rst split by heading). This is the floor to beat.
- `evaluation/run_eval.py`: runs the questions through our `RetrievalService` and reports accuracy, latency and provenance for semantic and hybrid search.

## Run against our pipeline

Needs Ollama running with `all-minilm` and the Chroma index built.

```bash
cd backend
uv run python -m document_digester.evaluation.run_eval
```

Only questions whose answer page is in the index get scored. The first line of output tells you how many.

## Run the baseline

```bash
cd backend
uv run --with sentence-transformers python -m document_digester.evaluation.baseline ~/path/to/godot-docs
```
