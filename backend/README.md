# Running the RAG app with a local Ollama model

1. Install Ollama (https://ollama.com/download), make sure it is running
   (`ollama serve`, or the tray app), and pull both models:

   ```powershell
   ollama pull all-minilm   # embeddings (retrieval)
   ollama pull llama3.2     # chat model (answer generation)
   ```

2. Index the docs (see below), then start the API from `backend/`:

   ```powershell
   uv run fastapi dev src/document_digester/api/main.py
   ```

3. Start the frontend from `frontend/` with `npm start` and open
   http://localhost:4200. The dev server proxies `/api` to port 8000.

`POST /api/chat` takes `{"query": "...", "top_k": 5, "history": [...]}`. It
retrieves chunks with hybrid (vector + BM25) search, sends them to the Ollama
LLM as context, and returns `{"answer": "...", "sources": [...]}`.

Optional settings go in environment variables or `backend/.env`:

| Variable | Default |
| --- | --- |
| `OLLAMA_BASE_URL` | `http://localhost:11434` |
| `LLM_MODEL` | `llama3.2` (any model from `ollama list`) |
| `LLM_TEMPERATURE` | `0.2` |
| `EMBEDDING_MODEL` | `all-minilm` (changing it requires re-indexing) |
| `DATABASE_URL` | unset. Only `/api/search/sql` and `/api/search/combined` use PostgreSQL. |

# Indexing the Godot documentation

The backend stores document chunks in a persistent local Chroma database. It
uses the configured Ollama embedding model both to find semantic chunk
boundaries and to embed chunks for Chroma.

1. Install Ollama, start its service, and download the configured embedding
   model (the default is `all-minilm`):

   ```powershell
   ollama pull all-minilm
   ```

2. From the `backend` directory, install the project dependencies and index
   the docs:

   ```powershell
   uv sync
   uv run python -m document_digester.service.ingestion.index_docs
   ```

The default Chroma database is stored under `backend/data/chroma/`. Override
the location with `CHROMA_PERSIST_DIRECTORY`, or select a different Ollama
embedding model with `EMBEDDING_MODEL`. Re-running the indexing command updates
the chunks associated with each source URL.

Each stored chunk includes its page title, source URL, `Header 2` and
`Header 3` section metadata, and chunk index. The page title is the document's
overall title; the heading metadata identifies its section. Chunks created
before the first matching heading use empty strings for missing heading levels.