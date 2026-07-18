from fastapi import FastAPI

app = FastAPI(
    title="CyberRAG API",
    version="0.1.0",
    description="AI-powered Cybersecurity Knowledge Assistant"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to CyberRAG API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
