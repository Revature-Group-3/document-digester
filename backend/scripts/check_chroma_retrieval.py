
from document_digester.retrieval import RetrievalService
from document_digester.settings import settings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model = settings.EMBEDDING_MODEL
)


#This is mock data for testing chroma
documents = [
    Document(
        page_content="Signals allow Godot nodes to communicate without directly referencing each other.",
        metadata={"source": "signals", "title": "Using Signals"}
    ),
    Document(
        page_content="The scene tree organizes nodes into parent-child relationships.",
        metadata={"source": "scene_tree", "title": "Scene Tree"}
    ),
    Document(
        page_content="CharacterBody2D is used to implement character movement and collision handling.",
        metadata={"source": "movement", "title": "Character Movement"}
    ),
    Document(
        page_content="AnimationPlayer allows you to create and control animations.",
        metadata={"source": "animation", "title": "Animation"}
    )
]

#A temporary in memory chroma collection.
#This does not modify Aarej's persistent db.
db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="retrieval_demo"
)

service = RetrievalService(db)

#This is the test prompt. It should return signals as the highest match. Should..
results = service.retrieve_top_k(
    "How can I send messages between nodes?",
    k=3
)

for result in results:
    print(f"\nRank: {result['rank']}")
    print(f"Text: {result['text']}")
    print(f"Source: {result['metadata'].get('source')}")
    print(f"Distance: {result['distance']:.4f}")

assert results[0]["metadata"]["source"] == "signals", (
    "Expected signals to be the highest-ranked result"
)

print("\nSemantic retrieval test passed!")

#This acts like a manual "smoke" test to see if it could work with a database.