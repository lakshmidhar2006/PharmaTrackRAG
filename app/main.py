# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api import documents, search, answer
from app.utils.metrics import setup_request_metrics
from app.config import settings

app = FastAPI(title="PharmaTrackRAG")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
app.mount("/metrics", make_asgi_app())

# Routers
app.include_router(documents.router, prefix="", tags=["documents"])
app.include_router(search.router, prefix="", tags=["search"])
app.include_router(answer.router, prefix="", tags=["answer"])


@app.get("/health")
async def health():
    return {"status": "ok"}


# Metrics middleware
setup_request_metrics(app)
