from fastapi import FastAPI
from document_digester.models import SearchRequest, SearchResponse

app = FastAPI(
    title="Documentation Digester",
    description="Semantic search for Godot documentation",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Documentation Digester API"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    results = []
    return SearchResponse(
        query=request.query,
        results=results
    )
