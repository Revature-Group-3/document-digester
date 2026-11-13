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
# Running the API

1. Create your environment file from the example (from the `backend` directory):

   ```powershell
   cp .env.example .env
   ```

   `DATABASE_URL` is required. A placeholder works for vector and hybrid
   search; SQL search needs a real Postgres connection string.

2. Index the docs (see above) so search has something to return.

3. Start the API from the `backend` directory:

   ```powershell
   uv run fastapi dev
   ```

   The app entrypoint is set in `pyproject.toml`, so no path is needed as long
   as you run it from `backend`. The interactive API docs are at
   http://127.0.0.1:8000/docs.
