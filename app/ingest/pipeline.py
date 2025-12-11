# app/ingest/pipeline.py

import uuid
from typing import List, Tuple
from app.ingest.parser import extract_text_from_pdf
from app.ingest.chunker import chunk_text
from app.services.embeddings import embed_texts
from app.services.faiss_store import add_vectors
from app.db.sqlite_client import get_conn
from app.utils.pii_redact import redact_pii


def ingest_document(document_id: str, path: str) -> int:
    """
    Full ingestion pipeline:
      1. extract text from file at `path`
      2. redact PII
      3. chunk text into (text, start_offset, end_offset)
      4. embed chunks
      5. add vectors to FAISS and get embedding indices
      6. persist chunk rows in SQLite with embedding index mapping

    Returns:
        number of chunks indexed
    """
    # 1. Extract text
    text = extract_text_from_pdf(path)

    # 2. Redact PII
    text = redact_pii(text)

    # 3. Chunk text
    chunks: List[Tuple[str, int, int]] = chunk_text(text)

    if not chunks:
        return 0

    # 4. Prepare texts and compute embeddings
    texts = [c[0] for c in chunks]
    embeddings = embed_texts(texts)  # returns numpy float32 array shape (n, dim)

    # 5. Add vectors to FAISS and get insertion indices
    indices = add_vectors(embeddings)  # list of int embedding indices

    # 6. Persist chunks to SQLite with embedding_index mapping
    conn = get_conn()
    cur = conn.cursor()
    try:
        for (chunk_text, start, end), emb_index in zip(chunks, indices):
            chunk_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO chunks (chunk_id, document_id, text, start_offset, end_offset, embedding_index) VALUES (?, ?, ?, ?, ?, ?)",
                (chunk_id, document_id, chunk_text, start, end, int(emb_index)),
            )
        conn.commit()
    finally:
        conn.close()

    return len(chunks)
