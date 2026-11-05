from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Python!"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}