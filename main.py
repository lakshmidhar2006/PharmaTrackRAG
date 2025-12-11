# app/main.py
from fastapi import FastAPI
app = FastAPI(title="PharmaTrackRAG")

@app.get("/health")
async def health():
    return {"status":"ok"}
